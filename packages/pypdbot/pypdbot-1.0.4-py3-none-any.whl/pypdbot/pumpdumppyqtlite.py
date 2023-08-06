# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 06:54:04 2020
@author: Ravi raj purohit
## TARNSFERRED TO PYQT GUI 
"""
import time, datetime
import requests#, threading
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow,\
                            QPushButton, QWidget, QFormLayout, \
                            QLineEdit, QToolBar, QStatusBar, \
                            QVBoxLayout, QTextEdit
import math
from twisted.internet import reactor, ssl
import numpy as np
import os
import _pickle as cPickle
import json

import hashlib
import hmac
from operator import itemgetter
import gzip
import threading
from autobahn.twisted.websocket import WebSocketClientFactory, \
                                        WebSocketClientProtocol, connectWS
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet.error import ReactorAlreadyRunning
# import ujson as json

import matplotlib
matplotlib.use('Qt5Agg')
matplotlib.rcParams.update({'font.size': 14})

from bs4 import BeautifulSoup
from PyQt5.QtCore import QSettings
import inspect
from PyQt5.QtWidgets import QComboBox, QCheckBox, QProgressBar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QGridLayout, QTableWidget, QTableWidgetItem
from selenium.webdriver.firefox.options import Options
import functools
from selenium import webdriver

current_pnl = 0.0

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

Logo = resource_path("logo.png")
BOT_START_TIME = time.time()
frame_title = "BinanceBot-Alpha"
#%% POST TREATMENT MODULE
def get_TVsignal(symbol, candle=[15]):
    ## symbol has to be TV compatible for Binance: BTCUSDTPERP
    ## candle data in minutes
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://scanner.tradingview.com/crypto/scan"
    cand = candle[0]

    payload =    {"symbols": {"tickers": ["BINANCE:{}".format(symbol+"PERP")],
                  "query": { "types": [] }},
                  "columns": ["BB.lower|{}".format(cand),
                              "BB.upper|{}".format(cand),
                              "close|{}".format(cand),
                              "close[1]|{}".format(cand),
                              "close[2]|{}".format(cand),
                              "open|{}".format(cand), ## current candle open
                              "open[1]|{}".format(cand),
                              "open[2]|{}".format(cand),
                              "BB.lower[1]|{}".format(cand),
                              "BB.upper[1]|{}".format(cand),
                              "BB.lower[2]|{}".format(cand),
                              "BB.upper[2]|{}".format(cand),]} ## previous candle open

    resp = requests.post(url,headers=headers,data=json.dumps(payload)).json()
    try:
        signal = resp["data"][0]["d"]
        # secondlastcandle = (signal[4] - signal[7]) > 0.0 ## green candle
        lastcandle = (signal[3] - signal[6]) > 0.0 ## green candle
        aboveBB = signal[3] > signal[9]
        var = lastcandle and aboveBB
        return var
    except:
        print("Error in the TradingView module for "+symbol)
        return False
    
class currency_container:
    def __init__(self, currencyArray, candle_len=10, mode = 'last_price'): 
        # v is quote volue (BTC), q is base value (USDT)
        self.symbol = currencyArray['s']
        initial_timestamp = time.time()
        self.time_stamp = initial_timestamp
        self.time_stamp_reset = initial_timestamp
        self.volume24hr = 0.0
        if mode == 'market':
            key = 'p'
        elif mode == 'last_price':
            key = 'c'
            keyV = "v"
            self.volume24hr = float(currencyArray[keyV])
        elif mode == 'bid':
            key = 'b'
        elif mode == 'ask':
            key = 'a'
        self.bid_price = float(currencyArray[key])
        self.price_time = [1.0 * float(currencyArray[key]) for _ in range(candle_len)]
        if mode == 'bid_ask':
            self.bid_price = (float(currencyArray['b']) + float(currencyArray['a'])) /2.
            self.price_time = [1.0 * (float(currencyArray['b']) + float(currencyArray['a'])) /2. for _ in range(candle_len)]
        self.time_stamp_period = [1.0 * initial_timestamp for _ in range(candle_len)]
        ### single price changes for different candles
        self.percent_chgsP = 0.0
        self.profit_percentP = 0.0
        # self.execute_trade = get_TVsignal(currencyArray['s'])
        self.execute_trade = False
        
class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        QMainWindow.__init__(self)
        
        app_icon = QtGui.QIcon()
        app_icon.addFile('logo.png', QtCore.QSize(16,16))
        self.setWindowIcon(app_icon)
        
        self.nb_trades = 0
        self.list_of_trades = []
        try:
            with open("active_trade.pickle", "rb") as input_file:
                self.trades_completed = cPickle.load(input_file)
        except:
            self.trades_completed = {}

        self.new_list = {}
        self.indicator = 'none'
        self.enabledT = False
        self.api = None
        self.state = 0
        self._sockets = {}
        self.popup_cnt = 0
        self.popup_cnt1 = 0
        self.running = False
        
        self.setWindowTitle(frame_title)
        # self._createMenu()
        self._createToolBar()
        self._createStatusBar()
        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.layout)
        self._createDisplay() ## display screen
        self.setDisplayText(frame_title)
        self.setDisplayText("GUI initialized! \nPlease configure bot settings first\n")
        self._formLayout() ## buttons and layout
        self.popups = []
        
        self.timer1temp = QtCore.QTimer()
        self.timer1temp.setInterval(int(5000))
        self.timer1temp.timeout.connect(self.update_)
        self.timer1temp.start()
    
    def update_(self,):
        with open("active_trade.pickle", "wb") as output_file:
            cPickle.dump(self.trades_completed, output_file)
    
    def closeEvent(self, event):
        # Return stdout to defaults.
        try:
            reactor.stop()
            self.on_manual_sell()
        except:
            pass
        self.close
        QApplication.closeAllWindows()
        super().closeEvent(event)
        
    def _createDisplay(self):
        """Create the display."""
        # Create the display widget
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        # Add the display to the general layout
        self.layout.addWidget(self.display)

    def setDisplayText(self, text):
        self.display.append('%s'%text)
        self.display.moveCursor(QtGui.QTextCursor.End)
        self.display.setFocus()

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

    def _createToolBar(self):
        self.tools = QToolBar()
        self.addToolBar(self.tools)
        self.trialtoolbar1 = self.tools.addAction('Price change plot', self.show_new_window)
        self.trialtoolbar2 = self.tools.addAction('Dynamic plot', self.show_new_window_dynamic)
        self.trialtoolbar4 = self.tools.addAction('Futures stat', self.show_new_window_dynamicFS)
        self.trialtoolbar3 = self.tools.addAction('Stats (several exchange)', self.show_new_window_dynamicBTC)
        self.trialtoolbar1.setEnabled(False)
        self.trialtoolbar2.setEnabled(False)
        self.trialtoolbar4.setEnabled(False)
        # self.trialtoolbar31.setEnabled(False)
    
    def show_new_window_nimpl(self):
        self.write_to_console("Functions not available as of now; in development", to_push=1)
    
    def show_new_window_sell(self, trades_completed):
        w9 = AnotherWindowsell(self.api, self.exchange, trades_completed)
        w9.show()
        self.popups.append(w9)    
    
    def show_new_windowtrade(self, trades_completed):
        w9 = AnotherWindowtrade(self.api, self.exchange, trades_completed)
        w9.show()
        self.popups.append(w9)
        
    def show_new_window(self):
        w = AnotherWindow(self.api, self.exchange)
        w.show()
        self.popups.append(w)
        
    def show_new_windowpnl(self):
        w123 = AnotherWindowpnl(self.api, self.exchange, BOT_START_TIME)
        w123.got_signal_socket.connect(self.postprocesspnl)
        w123.show()
        self.popups.append(w123)
        
    def show_new_window_dynamicBTC(self):
        w165 = AnotherWindowDynamicBTC(self.setDisplayText)
        w165.got_signal.connect(self.postprocessliq)
        w165.show()
        self.popups.append(w165)
    
    def show_new_window_dynamicFS(self):
        w1 = AnotherWindowDynamicFS(self.api)
        w1.got_text.connect(self.postprocessFS)
        w1.show()
        self.popups.append(w1)
        
    def show_new_window_dynamic(self):
        w175 = AnotherWindowDynamic(self.api, self.exchange)
        w175.show()
        self.popups.append(w175)
    
    def show_new_window_config(self):
        w2 = AnotherWindowConfig(self.api, state=self.state)
        w2.got_password.connect(self.postprocess)
        w2.show()
        self.state = self.state +1
        self.popups.append(w2)
    
    def postprocessFS(self, emit_dict):
        coins_ = np.array(emit_dict["coin"]).flatten()
        timeframe_ = np.array(emit_dict['TimeFrame']).flatten()
        trades1 = np.array(emit_dict['topLongShortAccountRatio']).flatten()
        trades2 = np.array(emit_dict['topLongShortPositionRatio']).flatten()
        trades3 = np.array(emit_dict['globalLongShortAccountRatio']).flatten()
        trades4 = np.array(emit_dict['takerlongshortRatio']).flatten()
        # every 5min and 1hour
        ind_ = trades1.argsort()[-5:][::-1]
        for i in ind_:
            line = coins_[i]+" has HIGHEST Long/Short ACCOUNT ratio in "+\
                                        timeframe_[0]+" timeframe with "+\
                                        str(trades1[i])
            self.write_to_console(line, to_push=1)
        self.write_to_console("\n", to_push=1)

        ind_ = trades2.argsort()[-5:][::-1]
        for i in ind_:
            line = coins_[i]+\
                                    " has HIGHEST Long/Short POSITION ratio in "+\
                                        timeframe_[0]+" timeframe with "+\
                                        str(trades2[i])
            self.write_to_console(line, to_push=1)
        self.write_to_console("\n", to_push=1)    

        ind_ = trades3.argsort()[-5:][::-1]
        for i in ind_:
            line = coins_[i]+\
                                    " has HIGHEST Long/Short GLOBAL ACCOUNT ratio in "+\
                                        timeframe_[0]+" timeframe with "+\
                                        str(trades3[i])
            self.write_to_console(line, to_push=1)
        self.write_to_console("\n", to_push=1)
        
        ind_ = trades4.argsort()[-5:][::-1]
        for i in ind_:
            line = coins_[i]+\
                                    " has HIGHEST BUY/SELL volume ratio in "+\
                                        timeframe_[0]+" timeframe with "+\
                                        str(trades4[i])
            self.write_to_console(line, to_push=1)
        self.write_to_console("\n", to_push=1)
            
    def postprocessliq(self, emit_dict):
        self.lim_trades = self.lim_trades + emit_dict["limtrades"]
        self.text1 = ["adding a shift in the market based on BTC movements"]
        self.usdt_addfunds = emit_dict["safety"]
        self.usdt_invest = emit_dict["investment"]
        if emit_dict["direction"] == "LONG":
            self.indicator = 'long'
            self.cb_strategy.setText("LONG")
        else:
            self.indicator = 'short'
            self.cb_strategy.setText("SHORT")
        self.cb_strategy.setReadOnly(True)
        # print status
        for line in self.text1:
            self.write_to_console(line, to_push=1)
    
    def postprocesspnl(self, emit_dict):
        symbol = emit_dict["signal"]
        #TODO
        # if symbol == "SOS":
        #     # tempp = self.api.futures_get_open_orders()
        #     # ss = []
        #     # for j in tempp:
        #     #     ss.append(j['symbol'])
        #     # ss = np.unique(ss)    
        #     # for i in ss:
        #     #     try:
        #     #         _  = self.api.futures_cancel_all_open_orders(symbol=i)
        #     #     except:
        #     #         pass
        #     # line = "SOS Liquidation approaching; cancelling all open orders"
        #     # self.write_to_console(line, to_push=1)
        # else:
        try:
            _  = self.api.futures_cancel_all_open_orders(symbol=symbol)
        except:
            line = "No open orders exists for "+symbol
            self.write_to_console(line, to_push=1)
        
        try:
            self.trades_completed[symbol]["trade_status"] = "finished"
        except:
            line = symbol + " doesn't exist in trade database; not managed by bot"
            self.write_to_console(line, to_push=1)
        self.update_()
        self.stop_ticker_symbol(symbol)  
    
    def postprocess(self, emit_dict):
        self.text1 = emit_dict["text1"]
        self.live_trade = emit_dict["live_trade"]
        self.take_profit = emit_dict["take_profit"]
        self.enabledT = emit_dict["enabledT"]
        self.bot_chatID = emit_dict["bot_chatID"]
        self.bot_token = emit_dict["bot_token"]
        self.ttp = emit_dict["ttp"]
        self.lim_trades = emit_dict["lim_trades"]
        self.profit_percent = emit_dict["profit_percent"]
        self.take_profit_trailing = emit_dict["take_profit_trailing"]
        self.safety_trade_percent = emit_dict["safety_trade_percent"]
        self.usdt_addfunds = emit_dict["usdt_addfunds"]
        self.usdt_invest = emit_dict["usdt_invest"]
        self.leverage = emit_dict["leverage"]
        self.lim_trades_per_coin = emit_dict["lim_trades_per_coin"]
        self.trade_per_coin = emit_dict["trade_per_coin"]
        self.coins = emit_dict["coins"]
        self.black_list = emit_dict["black_list"]
        self.api = emit_dict["binance_client"]
        bin_key = emit_dict["binance_key"]
        bin_secret = emit_dict["binance_secret"]
        self.price_analysis_mode = emit_dict["price_analysis_mode"]
        self.candlesP = emit_dict["candlesP"]
        self.is_exchange_market = emit_dict["is_exchange_market"]
        self.is_order_market = emit_dict["is_order_market"]
        self.basecurrency = emit_dict["basecurrency"] 
        self.mode_analysis = emit_dict["mode_analysis"] 
        
        if self.mode_analysis == "Automatic":
            self.price_pd.setEnabled(False)
            self.price_dp.setEnabled(False)
        else:
            self.price_pd.setEnabled(True)
            self.price_dp.setEnabled(True)
            
        if self.is_exchange_market:
            self.exchange = "FUTURES"
            if self.is_order_market:
                self.indicator = 'long'
            else:
                self.indicator = 'short'
            self.cb_exchange.setText("Binance Futures")
        else:
            self.exchange = "SPOT"
            self.leverage = 1
            self.indicator = 'long' # only long is allowed in spot
            self.cb_exchange.setText("Binance Spot")
        self.cb_exchange.setReadOnly(True)
        
        if self.is_order_market:
            self.cb_strategy.setText("LONG")
        else:
            self.cb_strategy.setText("SHORT")
        self.cb_strategy.setReadOnly(True)
        
        self.base_currencys.setText(self.basecurrency)
        self.base_currencys.setReadOnly(True)
        
        self.temp01.setText(str(self.live_trade))
        self.temp01.setReadOnly(True)
        self.temp02.setText(str(self.enabledT))
        self.temp02.setReadOnly(True)
        
        if bin_key != None and bin_secret != None:
            self.api_key_entry.setText(bin_key)
            self.api_key_entry.setEchoMode(QLineEdit.EchoMode.Password)
            self.api_key_entry.setReadOnly(True)
            self.api_secret_entry.setText(bin_secret)
            self.api_secret_entry.setEchoMode(QLineEdit.EchoMode.Password)
            self.api_secret_entry.setReadOnly(True)
        # print status
        for line in self.text1:
            self.write_to_console(line, to_push=1)
            
    def _createStatusBar(self):
        self.status = QStatusBar()
        self.status.showMessage("Bot status will be shown here")
        self.setStatusBar(self.status)

    def _formLayout(self):
        self.formLayout = QFormLayout()
        
        self.temp01 = QLineEdit()
        self.temp02 = QLineEdit()
        
        self.cb_exchange = QLineEdit()
        self.cb_strategy = QLineEdit()
        self.base_currencys = QLineEdit()
        # button for binance exchange connection
        self.btn = QPushButton('Connect to Exchange')
        self.btn.clicked.connect(self.on_connect_api)
        # self.btn.setEnabled(False)
        
        # button for bot start
        self.btn_bstart = QPushButton('Start bot')
        self.btn_bstart.clicked.connect(self.on_pump)
        # button for bot stop
        self.btn_bstop = QPushButton('Stop bot')
        self.btn_bstop.clicked.connect(self.on_manual_sell)
        self.btn_bstop.setEnabled(False)
        
        self.btn_bstoptp = QPushButton('Stop TP')
        self.btn_bstoptp.clicked.connect(self.stop_tp_sockets)
        self.btn_bstoptp.setEnabled(False)

        self.btn_config_trial = QPushButton('Configure bot settings (static and dynamic)')
        self.btn_config_trial.clicked.connect(self.show_new_window_config)
        ## api key and secret Qline
        self.api_key_entry = QLineEdit()
        self.api_secret_entry = QLineEdit()
        self.price_pd = QLineEdit() # auto_sell_spinbox
        self.price_dp = QLineEdit() # stop_loss_spinbox
        self.price_pd.setText("1.2")
        self.price_dp.setText("10")
        
        self.formLayout.addRow(self.btn_config_trial)
        self.formLayout.addRow('Exchange type:', self.cb_exchange)
        self.formLayout.addRow('Order strategy:', self.cb_strategy)
        self.formLayout.addRow('Trading currency:', self.base_currencys)
        self.formLayout.addRow('Exchange API key:', self.api_key_entry)
        self.formLayout.addRow('Exchange API secret:', self.api_secret_entry)
        self.formLayout.addRow('Live trade:', self.temp01)
        self.formLayout.addRow('Telegram:', self.temp02)
        self.formLayout.addRow('', self.btn)
        self.formLayout.addRow('Price change for PUMP/DUMP (%):', self.price_pd)
        self.formLayout.addRow('Price change for DUMP/PUMP (%):', self.price_dp)
        self.formLayout.addRow(self.btn_bstop, self.btn_bstart)
        self.formLayout.addRow("stop trailing profit socket", self.btn_bstoptp)
        self.layout.addLayout(self.formLayout)
        
    # BOT FUNCTIONS
    def stop_tp_sockets(self):
        try:
            for symbol in self._sockets:
                bm61 = self._sockets[symbol]["socketmanager"]
                key61 = self._sockets[symbol]["key"]
                bm61.stop_socket(key61)
                bm61.close()
                self._sockets[symbol]["socketmanager"] = ""
                self._sockets[symbol]["key"] = ""
                self.write_to_console("Socket closed for "+symbol, to_push=1)
        except:
            self.write_to_console("Socket is empty", to_push=1)
        
    def write_to_console(self, line, to_push=0):
        self.setDisplayText(str(line.encode('utf-8','ignore'),errors='ignore'))
        if self.enabledT and to_push==1:
            percent=str(line.encode('utf-8','ignore'),errors='ignore')
            send_text='https://api.telegram.org/bot' + self.bot_token + '/sendMessage?chat_id=' + self.bot_chatID + '&parse_mode=Markdown&text=' + percent
            requests.get(send_text)
    
    def precision_and_scale(self, x):
        max_digits = 14
        int_part = int(abs(x))
        magnitude = 1 if int_part == 0 else int(math.log10(int_part)) + 1
        if magnitude >= max_digits:
            return (magnitude, 0)
        frac_part = abs(x) - int_part
        multiplier = 10 ** (max_digits - magnitude)
        frac_digits = multiplier + int(multiplier * frac_part + 0.5)
        while frac_digits % 10 == 0:
            frac_digits /= 10
        scale = int(math.log10(frac_digits))
        return scale
    
    def on_connect_api(self):
        try:
            if self.api == None:
                self.write_to_console("Missing API info. Load config first", to_push=1) 
                return

            if self.is_exchange_market:
                info = self.api.futures_exchange_info()
                ## QUANTITY precision for Trailing stop market orders
                self.price_precision = {}
                self.quantity_precision = {}
                for s in info['symbols']:        
                    symbol = s['symbol']
                    self.quantity_precision[symbol] = s["quantityPrecision"]
                    for jj in s["filters"]:
                        if jj["filterType"] == "PRICE_FILTER":
                            self.price_precision[symbol] = self.precision_and_scale(float(jj["tickSize"]))
            else:
                info = self.api.get_exchange_info()
                ## QUANTITY precision for Trailing stop market orders
                self.price_precision = {}
                self.quantity_precision = {}
                for s in info['symbols']:        
                    symbol = s['symbol']
                    for ij in s['filters']:
                        if ij['filterType'] == "PRICE_FILTER":
                            self.price_precision[symbol] = self.precision_and_scale(float(ij["minPrice"]))
                        if ij['filterType'] == "LOT_SIZE":                        
                            self.quantity_precision[symbol] = self.precision_and_scale(float(ij["minQty"]))
                            
            if self.mode_analysis == "Automatic":
                self.price_pd.setEnabled(False)
                self.price_dp.setEnabled(False)
            else:
                self.price_pd.setEnabled(True)
                self.price_dp.setEnabled(True)
                
            self.btn_bstart.setEnabled(True)
            self.btn_bstop.setEnabled(True)
            self.btn.setEnabled(False)
            self.write_to_console("Connected to "+self.exchange+" API successfully.", to_push=1)
            self.write_to_console("Plots are available now", to_push=1)
            self.trialtoolbar1.setEnabled(True)
            self.trialtoolbar2.setEnabled(True)
            self.trialtoolbar4.setEnabled(True)
            # self.trialtoolbar31.setEnabled(True)
            if self.popup_cnt == 0:
                self.show_new_windowpnl()
                self.show_new_windowtrade(self.trades_completed)
                self.popup_cnt = 1
        except:
            self.write_to_console("Missing API info.", to_push=1)   
        ## print trade stats in table
        
    def disable_pre_pump_options(self,):
        self.price_pd.setEnabled(False)
        self.price_dp.setEnabled(False)
        self.btn_bstart.setEnabled(False)
        self.btn_bstop.setEnabled(True)
        self.btn.setEnabled(False)
        
    def enable_pump_options(self,):
        self.price_pd.setEnabled(True)
        self.price_dp.setEnabled(True)
        self.btn_bstart.setEnabled(True)
        self.btn_bstop.setEnabled(False)
        self.btn.setEnabled(True)

    #### Button Behaviour ####
    def on_pump(self):
        ct = time.time()
        now = datetime.datetime.fromtimestamp(ct)
        c_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        # c_time1 = now.strftime("%Y-%m-%d")
        self.filename_ = "trade_logs.txt"
        with open(self.filename_, "a") as myfile:
            myfile.write("# New trade logs @ "+ c_time +" \n")
        try:
            if self.popup_cnt1 == 0:
                self.popup_cnt1 = 1
                if self.is_exchange_market:
                    ### Checking to see if new threads for existing trades needed
                    if self.trades_completed != {}:
                        ## verify if position open
                        temp  = self.api.futures_position_information()
                        coins_symbol = [temp[i1]['symbol'] for i1 in range(len(temp)) \
                                        if float(temp[i1]['entryPrice']) != 0.0]
                            
                        for alt_coin in self.trades_completed:
                            if (self.trades_completed[alt_coin]["trade_status"] == "running") \
                                and (alt_coin in coins_symbol):
                                self.write_to_console("Retrieving previous trade for "+alt_coin, to_push=1)
                                ## start a socket manager to keep eye on the price movement
                                bm1 = BinanceSocketManager(self.api)
                                conn = bm1.start_symbol_mark_price_socket(symbol=alt_coin, \
                                                                          callback=self.sell_trailing_profit, fast=True)
                                self._sockets[alt_coin] = {"symbol": alt_coin, "socketmanager": bm1, "key": conn}
                                bm1.start()
                                time.sleep(.01)
                                self.write_to_console("Price socket started for "+alt_coin)
                                
                            if (self.trades_completed[alt_coin]["trade_status"] == "running") \
                                and (alt_coin not in coins_symbol):
                                _  = self.api.futures_cancel_all_open_orders(symbol=alt_coin)
                                self.trades_completed[alt_coin]["trade_status"] = "finished"
                                
                        self.write_to_console("Checking if any independent open orders are present.", to_push=1)
                        tempp = self.api.futures_get_open_orders()
                        ss = []
                        for j in tempp:
                            ss.append(j['symbol'])
                        ss = np.unique(ss)    
                        for i in ss:
                            if i not in coins_symbol:
                                _  = self.api.futures_cancel_all_open_orders(symbol=i)
                                line = "cancelling all open orders for "+i
                                self.write_to_console(line, to_push=1)
                    else:
                        self.write_to_console("No active trade found.", to_push=1)
                    
            self.disable_pre_pump_options()            
           
            try:
                percent = float(self.price_pd.text())
                percent1 = float(self.price_dp.text())
            except:
                self.write_to_console("Please fill the price change in numbers", to_push=1)
                return
            
            if (percent <= 0.0) or (percent1 <= 0.0):
                self.write_to_console("Price change percentage cannot be less than 0.", to_push=1)
                self.enable_pump_options()
                return
    
            self.write_to_console("Price based analysis started.", to_push=1)
            ### connect binance websocket
            self.bm = BinanceSocketManager(self.api)
            if (self.price_analysis_mode == "market"):
                self.conn_key = self.bm.start_all_mark_price_socket(self.process_message) #start_miniticker_socket
                self.btn_bstoptp.setEnabled(True)
            elif (self.price_analysis_mode == "last_price"):
                self.conn_key = self.bm.start_ticker_socket(self.process_message) #start_miniticker_socket
                self.btn_bstoptp.setEnabled(True)
            # elif (self.price_analysis_mode == "liquidation"):
            #     self.conn_key = self.bm.start_ticker_socket_allliq(self.process_message_liq)
            else:
                self.write_to_console("Not yet implemented, select last_price or market for price analysis in config!", to_push=1)
            self.bm.start()
            time.sleep(.01)
            self.write_to_console("Initialised successfully!", to_push=1)
            self.status.showMessage("Bot is running now!")
            
        except AttributeError:
            self.write_to_console("You need to connect to Binance before starting.", to_push=1)
            return
    
    def process_message_liq(self, msg): # TODO
        # sample stream OUTPUT
        # {'e': 'forceOrder', 'E': 1619351660699, 'o':
        # {'s': 'XRPUSDT', 'S': 'BUY', 'o': 'LIMIT',
        # 'f': 'IOC', 'q': '4386.3', 'p': '1.0775',
        # 'ap': '1.0711', 'X': 'FILLED',
        # 'l': '1536.7', 'z': '4386.3', 'T': 1619351660692}}
        print(msg)
    
    def on_manual_sell(self):
        self.enable_pump_options()
        self.write_to_console("Stopping the P and D detector for Price analysis", to_push=1)
        # reactor.stop()
        try: 
            self.bm.stop_socket(self.conn_key)
            self.bm.close()
        except:
            self.write_to_console("No socket is open.", to_push=1)
        self.status.showMessage("Bot is stopped now!")

    def limit_safety(self, alt_coin, units_old, statement, indicator_=None):
          statement.append("Placing Limit Safety Orders for "+alt_coin+"\n")
          # time.sleep(2)
          ## sleep for some seconds for the trade to be created
          leverage = self.leverage
          coin_trade = True
          merge_runningv1 = True
          
          loop_count = 0 ##0 to avoid forever loop
         
          while merge_runningv1:
              loop_count = loop_count + 1              
              if loop_count > 3:
                  merge_runningv1 = False

              try:
                  temp  = self.api.futures_position_information()
                  entry_price = [float(temp[i1]['entryPrice']) for i1 in range(len(temp)) \
                               if temp[i1]['symbol'] == alt_coin]
                  entry_price = entry_price[0]
              except:
                  statement.append("Error getting the entry price from Binance, trying again in 10seconds")
                  entry_price = 0.0
                  time.sleep(10)
                  continue

              if (coin_trade) and (entry_price > 0.0):
                  tab_cnt = 0                
                  ## scaled place safety order
                  if self.lim_trades_per_coin[alt_coin] > 1:
                      linspace = [self.usdt_invest + float(x)/(self.lim_trades_per_coin[alt_coin]-1)*\
                                  (self.usdt_addfunds-self.usdt_invest) \
                                      for x in range(self.lim_trades_per_coin[alt_coin])]
                  else:
                      linspace = [self.usdt_addfunds]
                 
                  nb_units = []
                  price_enter = []
                  units_price = []
                  ## first entry
                  nb_units.append(units_old)
                  price_enter.append(entry_price)
                  units_price.append(units_old*entry_price)  
                  for i in range(self.lim_trades_per_coin[alt_coin]):
                      if indicator_ == 'long':
                          entry_price1 = entry_price * (1 - ((self.safety_trade_percent/100.)*(i+1)))
                          type_ = "BUY"
                      elif indicator_ == 'short':
                          entry_price1 = entry_price * (1 + ((self.safety_trade_percent/100.)*(i+1)))
                          type_ = "SELL"
                     
                      if self.price_precision[alt_coin] == 0:
                          entry_price1 = int(entry_price1)
                      else:
                          entry_price1 = round(entry_price1, self.price_precision[alt_coin]) 
                      ### scaled safety trades
                      units = float(linspace[i]) / (entry_price1 / leverage)
                     
                      if self.quantity_precision[alt_coin] == 0:
                          units = int(units)
                      else:
                          units = round(units, self.quantity_precision[alt_coin]) 
                     
                      nb_units.append(units)
                      price_enter.append(entry_price1)
                      units_price.append(units*entry_price1)
                      
                      try:
                          _ = self.api.futures_create_order(symbol=alt_coin, side=type_, type="LIMIT", \
                                                            positionSide="BOTH", \
                                                            timeInForce="GTC", quantity=units, price=entry_price1)
                          tab_cnt = tab_cnt + 1
                      except:
                          statement.append("error during safety order placement \n")

                  if int(tab_cnt) == self.lim_trades_per_coin[alt_coin]:
                      self.trade_per_coin[alt_coin] = self.trade_per_coin[alt_coin] + 1
                      merge_runningv1 = False
                      coin_trade = False
                  else:
                      coin_trade = False
                      statement.append("Unkown error occured \n")
                      return statement
                     
                  qsd = ''
                  dsq = ''
                  for num, st in enumerate(linspace):
                      qsd = qsd+str(st)+'; '
                      u = nb_units[:num+2]
                      # p = price_enter[:num+2]
                      up = units_price[:num+2]
                      pr = sum(up)/sum(u) # sum(u*p)/sum(u)
                      dsq = dsq+str(round(pr,6))+'; '
                  statement.append("The entry price for "+alt_coin +" is "+str(entry_price)+"\n")
                  statement.append("Safety funds are added (with leverage of "+str(leverage)+\
                                   ") in the following order: "+qsd+"\n")

                  statement.append("The safety trades will bring the entry price for "+alt_coin +" to: "+dsq+"\n")
                  statement.append("Funds added to existing trade for "+alt_coin+"\n")
          statement.append("Exiting the sell Thread for "+alt_coin+"\n")
          return statement
      
    def _binance_buy_sell(self, alt_coin='BTCUSDT', current_value=0.0, \
                          statement=None, indicator_=None, ppercent=None):
        leverage = self.leverage
        ## we should probably add 0.5% price to the current price to account for a dump 
        try:
            if self.is_exchange_market:
                ## Making sure the trade being opened is CROSSED margin type
                temp_var = self.api.futures_change_margin_type(symbol=alt_coin, marginType="CROSSED")
                if temp_var['msg'] == 'success':
                    statement.append("Successfully updated the margin type to CROSSED for "+alt_coin+"\n")
        except:
            statement.append("Margin type is already set to CROSSED for "+alt_coin+"\n")
        ## change leverage of the coin
        
        try:
            if self.is_exchange_market:
                ## Making sure the trade being opened is CROSSED margin type
                temp_var = self.api.futures_change_leverage(symbol=alt_coin, leverage=int(leverage))
                statement.append("Successfully updated the leverage to "+str(temp_var["leverage"])+" for "+alt_coin+"\n")
        except:
            statement.append("Error during leverage setting for "+alt_coin+". PLEASE CHANGE MANUALLY \n")
        
        
        units = self.usdt_invest / (current_value / leverage)
        
        if self.quantity_precision[alt_coin] == 0:
            units = int(units)
        else:
            units = round(units, self.quantity_precision[alt_coin]) 
        
        if indicator_ == 'long':
            type_ = "BUY"
        elif indicator_ == 'short':
            type_ = "SELL"
        
        try: ## POSTING ORDERS IN BINANCE DIRECTLY
            if self.is_exchange_market:
                # Post order in futures
                data = self.api.futures_create_order(symbol=alt_coin, type="MARKET", quantity=units, \
                                                      positionSide="BOTH", side=type_)
                time.sleep(2)
                ## posting also limit safety orders for Futures
                if self.lim_trades_per_coin[alt_coin] > 0:
                    statement = self.limit_safety(alt_coin, units, statement, indicator_)
            else:
                # Post order in SPOT
                data = self.api.create_order(symbol=alt_coin, type="MARKET", quantity=units, \
                                                      side=type_)
        except BinanceAPIException as e:
            statement.append("Error in the Binance module while posting trades for "+alt_coin+"\n")
            statement.append(f"(Code {e.status_code}) {e.message}")
            return statement
        # time.sleep(2)
        
        # get order ID status    
        temp  = self.api.futures_position_information()
        entry_price_ = [[float(temp[i1]['entryPrice']),float(temp[i1]['positionAmt'])] \
                        for i1 in range(len(temp)) if temp[i1]['symbol'] == alt_coin]
        data["entry_price"] = entry_price_[0][0]
        data["entry_amount"] = entry_price_[0][1]
        data["units_total"] = entry_price_[0][1]
        
        if indicator_ == 'long':
            if ppercent == 0.0 or ppercent == None:
                sell_value = entry_price_[0][0] * (1 + (self.profit_percent/100.))
            else:
                sell_value = entry_price_[0][0] * (1 + (ppercent/100.))
            type_ = "SELL"
        elif indicator_ == 'short':
            if ppercent == 0.0 or ppercent == None:
                sell_value = entry_price_[0][0] * (1 - (self.profit_percent/100.))
            else:
                sell_value = entry_price_[0][0] * (1 - (ppercent/100.))
            type_ = "BUY"
            
        data["sell_value"] = sell_value
        data["type_"] = type_
        data["trade_time"] = time.time()
        data["count"] = 0
        data["ttp_activated"] = False
        data["old_price"] = 1e10
        data["trade_status"] = "running"
        data["safety_count"] = self.lim_trades_per_coin[alt_coin]
        
        self.trades_completed[alt_coin] = data
        self.update_()
        
        statement.append("New trade created in Binance for "+alt_coin+"\n")
        ## start a socket manager to keep eye on the price movement
        bm21 = BinanceSocketManager(self.api)
        conn21 = bm21.start_symbol_mark_price_socket(symbol=alt_coin, callback=self.sell_trailing_profit, fast=True)
        self._sockets[alt_coin] = {"symbol": alt_coin, "socketmanager": bm21, "key": conn21}
        bm21.start()
        time.sleep(.01)
        statement.append("Price socket started for "+alt_coin+"\n")
        return statement
    
    def stop_ticker_symbol(self, symbol):
        try:
            bm51 = self._sockets[symbol]["socketmanager"]
            key51 = self._sockets[symbol]["key"]
            bm51.stop_socket(key51)
            bm51.close()
            self._sockets[symbol]["socketmanager"] = ""
            self._sockets[symbol]["key"] = ""
            self.write_to_console("Socket closed for "+symbol, to_push=1)
        except:
            self.write_to_console("Socket is empty for "+symbol, to_push=1)
        
    def sell_trailing_profit(self, msg):
        
        symbol = msg["data"]['s']
        price = float(msg["data"]['p']) ## market price

        if self.trades_completed[symbol]["type_"] == "SELL" and self.trades_completed[symbol]["trade_status"]=="running":
            if price > self.trades_completed[symbol]["sell_value"]:
                if self.trades_completed[symbol]["count"] == 0:
                    temp  = self.api.futures_position_information()
                    entry_price_ = [[float(temp[i1]['entryPrice']),float(temp[i1]['positionAmt'])] \
                                    for i1 in range(len(temp)) if temp[i1]['symbol'] == symbol]
                    self.trades_completed[symbol]["units_total"] = entry_price_[0][1]
                    self.trades_completed[symbol]["count"] = 1
                    self.trades_completed[symbol]["ttp_activated"] = True
                    self.trades_completed[symbol]["old_price"] = np.copy(price)
                
                    if entry_price_[0][0] == 0:
                        _  = self.api.futures_cancel_all_open_orders(symbol=symbol)
                        ## stop the ticker stream
                        self.trades_completed[symbol]["trade_status"] = "finished"
                        self.update_()
                        self.stop_ticker_symbol(symbol)
                    
                if self.trades_completed[symbol]["ttp_activated"] and self.trades_completed[symbol]["trade_status"]=="running":
                    if price > self.trades_completed[symbol]["old_price"]*(1 + (self.take_profit_trailing/100.)):
                        self.trades_completed[symbol]["old_price"] = self.trades_completed[symbol]["old_price"]*(1 + (self.take_profit_trailing/100.))
                    
                    elif price < self.trades_completed[symbol]["old_price"] and self.trades_completed[symbol]["trade_status"]=="running":
                        self.trades_completed[symbol]["trade_status"] = "finished"
                        _ = self.api.futures_create_order(symbol=symbol, type="MARKET", 
                                                          quantity=self.trades_completed[symbol]["units_total"], \
                                                              positionSide="BOTH", side="SELL")
                        ## remove open orders from book
                        _  = self.api.futures_cancel_all_open_orders(symbol=symbol)
                        ## stop the ticker stream
                        self.update_()
                        self.stop_ticker_symbol(symbol)
                    
        elif self.trades_completed[symbol]["type_"] == "BUY" and self.trades_completed[symbol]["trade_status"]=="running":
            if price < self.trades_completed[symbol]["sell_value"]:
                if self.trades_completed[symbol]["count"] == 0:
                    temp  = self.api.futures_position_information()
                    entry_price_ = [[float(temp[i1]['entryPrice']),float(temp[i1]['positionAmt'])] \
                                    for i1 in range(len(temp)) if temp[i1]['symbol'] == symbol]
                    self.trades_completed[symbol]["units_total"] = abs(entry_price_[0][1])
                    self.trades_completed[symbol]["count"] = 1
                    self.trades_completed[symbol]["ttp_activated"] = True
                    self.trades_completed[symbol]["old_price"] = np.copy(price)
                
                    if entry_price_[0][0] == 0:
                        _  = self.api.futures_cancel_all_open_orders(symbol=symbol)
                        ## stop the ticker stream
                        self.trades_completed[symbol]["trade_status"] = "finished"
                        self.update_()
                        self.stop_ticker_symbol(symbol)
                    
                if self.trades_completed[symbol]["ttp_activated"] and self.trades_completed[symbol]["trade_status"]=="running":
                    if price < self.trades_completed[symbol]["old_price"]*(1 - (self.take_profit_trailing/100.)):
                        self.trades_completed[symbol]["old_price"] = self.trades_completed[symbol]["old_price"]*(1 - (self.take_profit_trailing/100.))
                    
                    elif price > self.trades_completed[symbol]["old_price"] and self.trades_completed[symbol]["trade_status"]=="running":
                        self.trades_completed[symbol]["trade_status"] = "finished"
                        _ = self.api.futures_create_order(symbol=symbol, type="MARKET", 
                                                          quantity=self.trades_completed[symbol]["units_total"], \
                                                      positionSide="BOTH", side="BUY")
                        ## remove open orders from book
                        _  = self.api.futures_cancel_all_open_orders(symbol=symbol)
                        ## stop the ticker stream
                        self.update_()
                        self.stop_ticker_symbol(symbol)

    def print_statement(self, c_time, symbol, flag1, volDiff1, volDiff, current_price, old_price, \
                        percent_chgsP, indicator_, ppercent):
        statement = []
        ## check open position counts (from Binance)
        coin_temp = []
        count = 10000000
        try:
            if self.is_exchange_market:
                temp  = self.api.futures_position_information()
                coin_temp = [temp[i1]['symbol'] for i1 in range(len(temp)) if float(temp[i1]['entryPrice']) != 0.0]
                count = len(coin_temp)
            statement.append("Current active smart trades in Binance is : "+str(count)+"\n")
        # TODO implement strategy for SPOT market
        except:
            statement.append("Problem collecting the open position history (Binance module); \
                              setting trade counts to 10000000 (i.e. cannot trade until Binance comes back online)\n")
        
        trade_log = False
        if symbol in coin_temp:
            statement.append("Order already open for this coin in Binance, doing nothing for "+symbol+"\n")
            
        elif (self.live_trade) and (count < self.lim_trades):
            self.nb_trades = self.nb_trades + 1
            statement = self._binance_buy_sell(alt_coin=symbol, \
                                                   current_value=current_price, \
                                                           statement=statement, \
                                                               indicator_=indicator_,\
                                                                   ppercent=ppercent)
            trade_log = True
                
        elif (count >= self.lim_trades):
            statement.append("Limit active trades in progress, will still continue with Safety for open trades")
            return
            
        sym = "SYM: " + symbol
        flag = "PRICE! ("+flag1+")"
        vDiff = "DIFF (%): " + str(round(volDiff, 2))
        pcci = "Old price: "+ str(old_price)
        pcci1 = "Current price: "+ str(current_price)
        curr_pd = "Current price change threshold: "+str(percent_chgsP)
        volval = ''
        if volDiff1 > 0.0:
            volval = "BUYING activity \n"
        elif volDiff1 < 0.0:
            volval = "SELLING activity \n"
            
        my_string = ' || '.join(map(str, [c_time, flag, sym, pcci, pcci1, curr_pd, vDiff, volval]))
        str_from_list = ''.join([data for ele in statement for data in ele])
        
        if trade_log:
            with open(self.filename_, "a") as myfile:
                myfile.write(my_string)
                myfile.write(str_from_list+" \n")
            
        self.write_to_console(str_from_list, to_push=1)
        self.write_to_console(my_string, to_push=1)
    
    def process_message(self, msg):
        if self.price_analysis_mode == "market":
            msg = msg["data"]
            
        ct = time.time()
        now = datetime.datetime.fromtimestamp(ct)
        c_time = now.strftime("%Y-%m-%d %H:%M:%S")
        
        for ijk in range(len(msg)):
            x = currency_container(msg[ijk], candle_len=len(self.candlesP), mode=self.price_analysis_mode)

            if (x.symbol not in self.coins) or x.symbol[-len(self.basecurrency):] != self.basecurrency:
                continue

            if x.symbol not in self.new_list:
                if self.mode_analysis == "Automatic":
                    if self.is_exchange_market:
                        trades= self.api.futures_klines(symbol=x.symbol, interval="1m", limit=1000)
                    else:
                        trades= self.api.get_klines(symbol=x.symbol, interval="1m", limit=1000)
                    ## candle stats
                    percentT = [100*(float(d[2]) - float(d[3]))/float(d[2]) for i, d in enumerate(trades)]
                    temp_ = [0.1 if np.mean(percentT) < 0.1 else np.mean(percentT)]
                    x.percent_chgsP = temp_[0]
                    x.profit_percentP = temp_[0]
                else:
                    x.percent_chgsP = float(self.price_pd.text())
                
                self.new_list[x.symbol] = x
                self.write_to_console("Gathering (only "+self.basecurrency+" pairs) "+x.symbol, to_push=1)
            
            else:
                stored_currency = self.new_list[x.symbol]
                
                indicator_ = np.copy(self.indicator) #Perm copy
                
                if ((ct - stored_currency.time_stamp) > 1):
                    stored_currency.time_stamp = ct 

                    for i in range(len(stored_currency.time_stamp_period)):
                        
                        if ((ct - stored_currency.time_stamp_period[i]) >= self.candlesP[i]):
                            
                            execute_trade = False
                            
                            priceDiff1 = ((x.bid_price - stored_currency.price_time[i]) / stored_currency.price_time[i]) * 100                              
                            # temp var to launch
                            if self.mode_analysis == "Automatic":
                                if indicator_ == 'long':
                                    pd_val = stored_currency.percent_chgsP
                                    dp_val = pd_val * 50 # some high value
                                else:
                                    dp_val = stored_currency.percent_chgsP
                                    pd_val = pd_val * 50 # some high value
                            else:
                                pd_val = self.price_pd.text()
                                dp_val = self.price_dp.text()
                                
                            if ((priceDiff1 < 0.0) and (abs(priceDiff1) > float(dp_val))) or \
                                ((priceDiff1 > 0.0) and (float(dp_val) > abs(priceDiff1) > float(pd_val))):
                                ## big DUMP or small PUMP (open a LONG)
                                if indicator_ == 'long':
                                    execute_trade = True
                                elif indicator_ == 'short':
                                    execute_trade = False
                                
                            elif ((priceDiff1 < 0.0) and (float(dp_val) > abs(priceDiff1) > float(pd_val))) or \
                                ((priceDiff1 > 0.0) and (abs(priceDiff1) > float(dp_val))):
                                ## small DUMP or big PUMP (open a SHORT)
                                if indicator_ == 'short':
                                    execute_trade = True
                                elif indicator_ == 'long':
                                    execute_trade = False
                                
                            # if ((ct - stored_currency.time_stamp_reset) > 15*60):
                            #     stored_currency.time_stamp_reset = ct
                            #     stored_currency.execute_trade = get_TVsignal(x.symbol)
                            
                            if (execute_trade or stored_currency.execute_trade) and self.running==False:
                                self.running = True
                                self.print_statement(c_time, stored_currency.symbol, \
                                                    str(self.candlesP[i])+" Sec", \
                                                    priceDiff1, abs(priceDiff1), \
                                                    x.bid_price,stored_currency.price_time[i],\
                                                    stored_currency.percent_chgsP, indicator_,
                                                    stored_currency.profit_percentP)
                                stored_currency.time_stamp_period =  [ct for _ in range(len(self.candlesP))]
                                stored_currency.price_time =  [x.bid_price for _ in range(len(self.candlesP))]
                                self.running = False
                                
                            stored_currency.price_time[i] = x.bid_price
                            stored_currency.time_stamp_period[i] = ct   
                    stored_currency.volume24hr = x.volume24hr
                    
                if ((ct - stored_currency.time_stamp_reset) > 3600):
                    stored_currency.time_stamp_reset = ct
                    if self.mode_analysis == "Automatic":
                        if self.is_exchange_market:
                            trades= self.api.futures_klines(symbol=x.symbol, interval="1m", limit=1000)
                        else:
                            trades= self.api.get_klines(symbol=x.symbol, interval="1m", limit=1000)
                        ## candle stats
                        percentT = [100*(float(d[2]) - float(d[3]))/float(d[2]) for i, d in enumerate(trades)]
                        temp_ = [0.1 if np.mean(percentT) < 0.1 else np.mean(percentT)]
                        stored_currency.percent_chgsP = temp_[0]
                        stored_currency.profit_percentP = temp_[0]
                    else:
                        stored_currency.percent_chgsP = float(self.price_pd.text())

class AnotherWindowtrade(QWidget):
    # Override class constructor
    def __init__(self, binance_api=None, exchange=None, trades_completed=None):
        super().__init__()
        app_icon = QtGui.QIcon()
        app_icon.addFile('logo.png', QtCore.QSize(16,16))
        # You must call the super class method
        # self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        # self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        self.setWindowTitle("Trade stats")    # Set the window title
        self.setWindowIcon(app_icon)
        self.api = binance_api
        grid_layout = QGridLayout(self)  # Create QGridLayout

        self.table = QTableWidget(self)  # Create a table
        self.table.setColumnCount(8)     # Set three columns
        self.table.setRowCount(20)       # and one row

        # Set the table headers
        self.table.setHorizontalHeaderLabels(["Managed by BOT", "Symbol", "Size", "Entry price", 
                                         "Current price", "PnL", "safety left",
                                         "Trailing profit"])

        grid_layout.addWidget(self.table, 0, 0)   # Adding the table to the grid
        
        self._socketsw = {}
        if exchange == "FUTURES":
            ## process information for relevant timestamp
            info = self.api.futures_account_balance()
            self.wallet_balance = float(info[1]["balance"])
            self.wallet_balancebnb = float(info[0]["balance"])
            
            self.coin_id = {}
            ## verify if position open
            temp  = self.api.futures_position_information()
            coins_symbol = [temp[i1]['symbol'] for i1 in range(len(temp)) \
                            if float(temp[i1]['entryPrice']) != 0.0]
            id_ = 0     
            active_trade_list = []
            if trades_completed != {}:
                for alt_coin in trades_completed:
                    if (trades_completed[alt_coin]["trade_status"] == "running") \
                        and (alt_coin in coins_symbol):
                        active_trade_list.append(alt_coin)
                        entry_price_ = [[float(temp[i1]['entryPrice']),float(temp[i1]['positionAmt'])] \
                                for i1 in range(len(temp)) if temp[i1]['symbol'] == alt_coin]                            
                        data = trades_completed[alt_coin]
                        temp_p = self.api.futures_get_open_orders(symbol=alt_coin)
                        self.table.setItem(id_, 6, QTableWidgetItem(str(len(temp_p))))
                                         
                        self.table.setItem(id_, 0, QTableWidgetItem("True"))
                        self.table.item(id_, 0).setBackground(QtCore.Qt.green)
                        self.table.setItem(id_, 1, QTableWidgetItem(alt_coin))
                        if data["type_"] == "SELL":
                            self.table.item(id_, 1).setBackground(QtCore.Qt.green)
                        else:
                            self.table.item(id_, 1).setBackground(QtCore.Qt.red)      
                        self.table.setItem(id_, 2, QTableWidgetItem(str(entry_price_[0][1])))
                        self.table.setItem(id_, 3, QTableWidgetItem(str(entry_price_[0][0])))
                        self.table.setItem(id_, 7, QTableWidgetItem(str(data["sell_value"])))
                        self.coin_id[alt_coin] = {"id":id_, "entry": entry_price_[0][0],
                                                  "units": entry_price_[0][1], "price":0,
                                                  "pnl":0} 
                        ## start a socket manager to keep eye on the price movement
                        bm1 = BinanceSocketManager(self.api)
                        conn = bm1.start_symbol_mark_price_socket(symbol=alt_coin, \
                                                                  callback=self.update_table, fast=True)
                        self._socketsw[alt_coin] = {"symbol": alt_coin, "socketmanager": bm1, "key": conn}
                        bm1.start()
                        time.sleep(.01)
                        id_ = id_ + 1
                        
            for alt_coin in coins_symbol:
                if (alt_coin not in active_trade_list):
                    entry_price_ = [[float(temp[i1]['entryPrice']),float(temp[i1]['positionAmt'])] \
                                for i1 in range(len(temp)) if temp[i1]['symbol'] == alt_coin]
                    temp_p = self.api.futures_get_open_orders(symbol=alt_coin)
                    self.table.setItem(id_, 6, QTableWidgetItem(str(len(temp_p))))
                    self.table.setItem(id_, 0, QTableWidgetItem("False"))
                    self.table.item(id_, 0).setBackground(QtCore.Qt.red)
                    self.table.setItem(id_, 1, QTableWidgetItem(alt_coin))     
                    self.table.setItem(id_, 2, QTableWidgetItem(str(entry_price_[0][1])))
                    self.table.setItem(id_, 3, QTableWidgetItem(str(entry_price_[0][0])))
                    self.table.setItem(id_, 7, QTableWidgetItem(str("None")))
                    self.coin_id[alt_coin] = {"id":id_, "entry": entry_price_[0][0],
                                            "units": entry_price_[0][1], "price":0,
                                            "pnl":0}  ## row at which that coin is present
                    ## start a socket manager to keep eye on the price movement
                    bm11 = BinanceSocketManager(self.api)
                    conn11 = bm11.start_symbol_mark_price_socket(symbol=alt_coin, \
                                                              callback=self.update_table, fast=True)
                    self._socketsw[alt_coin] = {"symbol": alt_coin, "socketmanager": bm11, "key": conn11}
                    bm11.start()
                    time.sleep(.01)
                    id_ = id_ + 1    
            self.bm546 = BinanceSocketManager(self.api)
            self.conn_key546 = self.bm546.start_futures_user_socket(self.replot_table)
            self.bm546.start()
        elif exchange == "SPOT":
            # TODO
            ## Not implemented yet
            info = self.api.get_exchange_info()
            return
        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer100 = QtCore.QTimer()
        self.timer100.setInterval(int(1000))
        self.timer100.timeout.connect(self.update_tab)
        self.timer100.start()
        
    def replot_table(self, msg):            
        if msg["e"] == "ORDER_TRADE_UPDATE":
            temp_ = msg["o"]
            
            if (temp_['X'] == "FILLED"):
                time.sleep(5)
                self.table.clearContents()
                self.table.setRowCount(0)       # and one row
                self.table.setRowCount(20)       # and one row
                try:
                    with open("active_trade.pickle", "rb") as input_file:
                        trades_completed = cPickle.load(input_file)
                except:
                    trades_completed = {}
                ## verify if position open
                temp  = self.api.futures_position_information()
                coins_symbol = [temp[i1]['symbol'] for i1 in range(len(temp)) \
                                if float(temp[i1]['entryPrice']) != 0.0]                    
                id_ = 0
                active_trade_list = []
                self.coin_id = {}
                if trades_completed != {}:
                    for alt_coin in trades_completed:
                        if (trades_completed[alt_coin]["trade_status"] == "running") \
                            and (alt_coin in coins_symbol):
                            active_trade_list.append(alt_coin)
                            entry_price_ = [[float(temp[i1]['entryPrice']),float(temp[i1]['positionAmt'])] \
                                    for i1 in range(len(temp)) if temp[i1]['symbol'] == alt_coin]                            
                            data = trades_completed[alt_coin]                        
                            self.table.setItem(id_, 0, QTableWidgetItem("True"))
                            self.table.item(id_, 0).setBackground(QtCore.Qt.green)
                            
                            temp_p = self.api.futures_get_open_orders(symbol=alt_coin)
                            self.table.setItem(id_, 6, QTableWidgetItem(str(len(temp_p))))
                        
                            self.table.setItem(id_, 1, QTableWidgetItem(alt_coin))
                            if data["type_"] == "SELL":
                                self.table.item(id_, 1).setBackground(QtCore.Qt.green)
                            else:
                                self.table.item(id_, 1).setBackground(QtCore.Qt.red)      
                                
                            self.table.setItem(id_, 2, QTableWidgetItem(str(entry_price_[0][1])))
                            self.table.setItem(id_, 3, QTableWidgetItem(str(entry_price_[0][0])))
                            self.table.setItem(id_, 7, QTableWidgetItem(str(data["sell_value"])))
                            self.coin_id[alt_coin] = {"id":id_, "entry": entry_price_[0][0],
                                                      "units": entry_price_[0][1], "price":0,
                                                      "pnl":0} 
                            ## start a socket manager to keep eye on the price movement
                            if alt_coin not in self._socketsw:
                                bm1 = BinanceSocketManager(self.api)
                                conn = bm1.start_symbol_mark_price_socket(symbol=alt_coin, \
                                                                          callback=self.update_table, fast=True)
                                self._socketsw[alt_coin] = {"symbol": alt_coin, "socketmanager": bm1, "key": conn}
                                bm1.start()
                                time.sleep(.01)
                            id_ = id_ + 1
                            
                for alt_coin in coins_symbol:
                    if (alt_coin not in active_trade_list):
                        entry_price_ = [[float(temp[i1]['entryPrice']),float(temp[i1]['positionAmt'])] \
                                            for i1 in range(len(temp)) if temp[i1]['symbol'] == alt_coin]                            
                        temp_p = self.api.futures_get_open_orders(symbol=alt_coin)
                        self.table.setItem(id_, 6, QTableWidgetItem(str(len(temp_p))))                      
                        self.table.setItem(id_, 0, QTableWidgetItem("False"))
                        self.table.item(id_, 0).setBackground(QtCore.Qt.red)
                        self.table.setItem(id_, 1, QTableWidgetItem(alt_coin))     
                        self.table.setItem(id_, 2, QTableWidgetItem(str(entry_price_[0][1])))
                        self.table.setItem(id_, 3, QTableWidgetItem(str(entry_price_[0][0])))
                        self.table.setItem(id_, 7, QTableWidgetItem(str("None")))
                        self.coin_id[alt_coin] = {"id":id_, "entry": entry_price_[0][0],
                                                "units": entry_price_[0][1], "price":0,
                                                "pnl":0}  ## row at which that coin is present
                        ## start a socket manager to keep eye on the price movement
                        if alt_coin not in self._socketsw:
                            bm121 = BinanceSocketManager(self.api)
                            conn121 = bm121.start_symbol_mark_price_socket(symbol=alt_coin, \
                                                                      callback=self.update_table, fast=True)
                            self._socketsw[alt_coin] = {"symbol": alt_coin, "socketmanager": bm121, "key": conn121}
                            bm121.start()
                            time.sleep(.01)
                        id_ = id_ + 1
                        
                for alt_coin in self._socketsw:
                    if alt_coin not in coins_symbol:
                        try:
                            bm147 = self._socketsw[alt_coin]["socketmanager"]
                            key147 = self._socketsw[alt_coin]["key"]
                            bm147.stop_socket(key147)
                            bm147.close()
                            self._socketsw[alt_coin]["socketmanager"] = ""
                            self._socketsw[alt_coin]["key"] = ""
                        except:
                            pass
    
    def update_tab(self):
        try:
            global current_pnl
            current_pnl = 0.0
            for altcoin in self.coin_id:
                id_ = self.coin_id[altcoin]["id"]
                price = self.coin_id[altcoin]["price"]
                pnl = round(self.coin_id[altcoin]["pnl"],2)
                current_pnl = current_pnl + pnl
                self.table.setItem(id_, 4, QTableWidgetItem(str(price)))
                self.table.setItem(id_, 5, QTableWidgetItem(str(pnl)))
                if pnl > 0:
                    self.table.item(id_, 5).setBackground(QtCore.Qt.green)
                else:
                    self.table.item(id_, 5).setBackground(QtCore.Qt.red)
        except:
            pass
    
    def update_table(self, msg):
        symbol = msg["data"]['s']
        price = float(msg["data"]['p']) ## market price
        pnl = (price - self.coin_id[symbol]["entry"]) * self.coin_id[symbol]["units"]
        self.coin_id[symbol]["price"] = price
        self.coin_id[symbol]["pnl"] = pnl        
        
    def closeEvent(self, event):
        try:
            for symbol in self._socketsw:
                bm987 = self._socketsw[symbol]["socketmanager"]
                key987 = self._socketsw[symbol]["key"]
                bm987.stop_socket(key987)
                bm987.close()
                self._socketsw[symbol]["socketmanager"] = ""
                self._socketsw[symbol]["key"] = ""
            self.bm546.stop_socket(self.conn_key546)
            self.bm546.close()
        except:
            pass
        self.close()
        
class AnotherWindowsell(QWidget):
    # Override class constructor
    def __init__(self, binance_api=None, exchange=None, trades_completed=None):
        super().__init__()
        app_icon = QtGui.QIcon()
        app_icon.addFile('logo.png', QtCore.QSize(16,16))
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        self.setWindowTitle("Trade stats")    # Set the window title
        self.setWindowIcon(app_icon)
        
        self.api = binance_api
        
        self.layout = QVBoxLayout()

        formLayout = QFormLayout()
        formLayout.addRow('COIN symbol (exhaustive list):', self.cb_strategy1)
        formLayout.addRow('COIN symbol (or manual):', self.coin_name)
        formLayout.addRow('Time interval:', self.cb_strategy)
        formLayout.addRow('Bin length (in integer):', self.bin)
        formLayout.addRow('Nb of candles (in integer):', self.candles)
        formLayout.addRow(self.btn_config)      
        
        self.layout.addLayout(formLayout, 0)
        self.setLayout(self.layout)

        self.total_port = QLineEdit() # 
        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer100 = QtCore.QTimer()
        self.timer100.setInterval(int(1000))
        self.timer100.timeout.connect(self.update_tab)
        self.timer100.start()
        
    def replot_table(self, msg):            
        pass
    
    def update_tab(self):
        pass
    
    def update_table(self, msg):
        pass       
        
    def closeEvent(self, event):
        pass 
        
#% MAIN GUI
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, subplot=2):
        fig = Figure(figsize=(width, height), dpi=dpi)
        if subplot == 1:
            self.axes = fig.add_subplot(111)
        else:
            self.axes = fig.add_subplot(211)
            self.axes1 = fig.add_subplot(212)
        super(MplCanvas, self).__init__(fig)

class AnotherWindowpnl(QWidget):
    got_signal_socket = QtCore.pyqtSignal(dict)
    
    def __init__(self, binance_api=None, exchange=None, BOT_START_TIME=None):
        super().__init__()
        app_icon = QtGui.QIcon()
        app_icon.addFile('logo.png', QtCore.QSize(16,16))
        self.setMinimumSize(QtCore.QSize(480, 80)) 
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        # self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        
        self.setWindowIcon(app_icon)
        self._exchange = exchange
        self.api = binance_api
        self.bot_start_time = BOT_START_TIME
        
        self.profit_ = {}
        self.commission_ = {}
        self.commissionbnb_ = {}
        self.ff1_ = 0.0
        self.update = False
        self.wallet_balance = 0
        
        # now = datetime.datetime.fromtimestamp(self.bot_start_time)
        # c_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        # self.filename_ = "trade_stats_"+c_time+".txt"
        self.filename_ = "trade_stats.pickle"
        ## load and get old data from trade stats file
        try:
            with open(self.filename_, "rb") as input_file:
                pp1, cc1, cc1b, ff1 = cPickle.load(input_file)
        except:
            pp1, cc1, cc1b, ff1 = {}, {}, {}, 0.0

        if exchange == "FUTURES":
            self.bm123 = BinanceSocketManager(self.api)
            self.conn_key123 = self.bm123.start_futures_user_socket(self.plot_pc)
            self.bm123.start()
            ## process information for relevant timestamp
            info = self.api.futures_account_balance()
            self.wallet_balance = float(info[1]["balance"])
            self.wallet_balancebnb = float(info[0]["balance"])
            
            info = self.api.futures_exchange_info()
            for s in info['symbols']:
                try:
                    self.profit_[s['symbol']] = float(pp1[s['symbol']])
                except:
                    self.profit_[s['symbol']] = 0.0
                    
                try:
                    self.commission_[s['symbol']] = float(cc1[s['symbol']])
                except:
                    self.commission_[s['symbol']] = 0.0
                
                try:
                    self.commissionbnb_[s['symbol']] = float(cc1b[s['symbol']])
                except:
                    self.commissionbnb_[s['symbol']] = 0.0
                    
                try:
                    self.ff1_ = float(ff1)
                except:
                    self.ff1_ = 0.0
                    
        elif exchange == "SPOT":
            # TODO
            ## Not implemented yet
            info = self.api.get_exchange_info()
            return
        
        self.total_port = QLineEdit() # 
        self.total_portbnb = QLineEdit() # 
        self.unreal_pnl = QLineEdit() # 
        self.profits = QLineEdit() # 
        self.fundfee = QLineEdit() # 
        self.commission = QLineEdit() # 
        self.commissionbnb = QLineEdit() 
        self.current_pnl = QLineEdit() 
        self.avail_balance = QLineEdit() 
        
        self.total_port.setReadOnly(True)
        self.total_portbnb.setReadOnly(True)
        self.unreal_pnl.setReadOnly(True)
        self.profits.setReadOnly(True)
        self.fundfee.setReadOnly(True)
        self.commission.setReadOnly(True)
        self.commissionbnb.setReadOnly(True)
        self.current_pnl.setReadOnly(True)
        self.avail_balance.setReadOnly(True)
        
        self.total_port.setText(str(self.wallet_balance))
        self.total_portbnb.setText(str(self.wallet_balancebnb))
        self.profits.setText("0.0")
        self.fundfee.setText("0.0")
        self.commission.setText("0.0")
        self.commissionbnb.setText("0.0")
        self.current_pnl.setText("0.0")
        self.avail_balance.setText(str(self.wallet_balance))
        
        self.layout = QVBoxLayout()
        
        formLayout = QFormLayout()
        formLayout.addRow('Total (USDT):', self.total_port)
        formLayout.addRow('Total (BNB):', self.total_portbnb)
        formLayout.addRow('Current PnL (USDT):', self.current_pnl)
        formLayout.addRow('Available balance (USDT):', self.avail_balance)
        formLayout.addRow('Profit (USDT):', self.profits)
        formLayout.addRow('Funding fee (USDT):', self.fundfee)
        formLayout.addRow('Commissions (USDT):', self.commission)
        formLayout.addRow('Commissions (BNB):', self.commissionbnb)
        
        
        self.layout.addLayout(formLayout, 0)
        self.setLayout(self.layout)
        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer_count = 0
        self.timer1 = QtCore.QTimer()
        self.timer1.setInterval(int(1000))
        self.timer1.timeout.connect(self.plot_pcv11)
        self.timer1.start()
        
    def closeEvent(self, event):
        self.timer1.stop()
        self.bm123.stop_socket(self.conn_key123)
        self.bm123.close()
        self.close()
    
    def plot_pcv11(self):
        global current_pnl
        self.timer_count = self.timer_count + 1
        if self.timer_count > 360:
            info = self.api.futures_account_balance()
            avail_bal = float(info[1]["availableBalance"])
            self.timer_count = 0
            if avail_bal < 1000:
                emit_dict = {"signal": "SOS"}
                self.got_signal_socket.emit(emit_dict)

        values = self.profit_.values()
        income = sum(values)
        valuescs = self.commission_.values()
        cs = sum(valuescs)
        valuescsb = self.commissionbnb_.values()
        csb = sum(valuescsb)
        ff = self.ff1_
        
        self.total_port.setText(str(self.wallet_balance))
        self.avail_balance.setText(str(self.wallet_balance + current_pnl))
        self.profits.setText(str(income))
        self.fundfee.setText(str(ff))
        self.commission.setText(str(cs))
        self.total_portbnb.setText(str(self.wallet_balancebnb))
        self.commissionbnb.setText(str(csb))
        self.current_pnl.setText(str(current_pnl))
        
        if self.update:
            with open(self.filename_, "wb") as output_file:
                cPickle.dump([self.profit_, self.commission_, self.commissionbnb_, self.ff1_], output_file)
            self.update = False

    ## WEBSOCKET VERSION  
    def plot_pc(self, msg):
        if msg["e"] == "ACCOUNT_UPDATE":
            if msg["a"]["m"] == "FUNDING_FEE":
                old_balance = np.copy(self.wallet_balance)
                funding_f = old_balance - float(msg["a"]["B"][0]["wb"])
                self.ff1_ = self.ff1_ + funding_f
                
            if msg["a"]["B"][0]["a"] == "USDT":
                self.wallet_balance = float(msg["a"]["B"][0]["wb"])
            if msg["a"]["B"][0]["a"] == "BNB":
                self.wallet_balancebnb = float(msg["a"]["B"][0]["wb"])
                
        if msg["e"] == "ORDER_TRADE_UPDATE":
            temp_ = msg["o"]
            if temp_['x'] == "TRADE" and (temp_['X'] == "FILLED" or temp_['X'] == "PARTIALLY_FILLED"):
                coin_ = temp_['s']
                self.profit_[coin_] = self.profit_[coin_] + float(temp_['rp'])
                if temp_['N'] == "USDT":
                    self.commission_[coin_] = self.commission_[coin_] + float(temp_['n'])
                elif temp_['N'] == "BNB":
                    self.commissionbnb_[coin_] = self.commissionbnb_[coin_] + float(temp_['n'])
                self.update = True
                
            if (temp_['X'] == "FILLED") and (float(temp_['rp']) != 0):
            ## close open trades for the coin
            ## send a command to the main parent
                emit_dict = {"signal": temp_['s']}
                self.got_signal_socket.emit(emit_dict)
        
class AnotherWindow(QWidget):
    def __init__(self, binance_api=None, exchange=None):
        super().__init__()
        app_icon = QtGui.QIcon()
        app_icon.addFile('logo.png', QtCore.QSize(16,16))
        self.setWindowIcon(app_icon)
        self._exchange = exchange
        self.api = binance_api
        if exchange == "FUTURES":
            info = self.api.futures_exchange_info()
        elif exchange == "SPOT":
            info = self.api.get_exchange_info()
            
        self.cb_strategy = QComboBox()
        self.cb_strategy.addItem("1m")
        self.cb_strategy.addItem("5m")
        self.cb_strategy.addItem("15m")
        self.cb_strategy.addItem("30m")
        
        self.cb_strategy1 = QComboBox()
        for s in info['symbols']:
            self.cb_strategy1.addItem(s['symbol'])

        self.coin_name = QLineEdit() # auto_sell_spinbox
        self.bin = QLineEdit() # stop_loss_spinbox
        self.candles = QLineEdit() # stop_loss_spinbox
        
        self.coin_name.setText("none")
        self.bin.setText("180")
        self.candles.setText("1500")
        # button for load config file
        self.btn_config = QPushButton('Plot')
        self.btn_config.clicked.connect(self.plot_pc)
        
        self.layout = QVBoxLayout()
        # self.layout.setSpacing(0)
        # self.layout.setMargin(0)
        # a figure instance to plot on
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)        
        # set the layout
        self.layout.addWidget(self.toolbar, 0)
        self.layout.addWidget(self.canvas, 100)
        
        formLayout = QFormLayout()
        formLayout.addRow('COIN symbol (exhaustive list):', self.cb_strategy1)
        formLayout.addRow('COIN symbol (or manual):', self.coin_name)
        formLayout.addRow('Time interval:', self.cb_strategy)
        formLayout.addRow('Bin length (in integer):', self.bin)
        formLayout.addRow('Nb of candles (in integer):', self.candles)
        formLayout.addRow(self.btn_config)      
        
        self.layout.addLayout(formLayout, 0)
        self.setLayout(self.layout)
        
    def plot_pc(self):
        self.canvas.figure.clf() 
        
        self.time_interval = self.cb_strategy.currentText()
        self.candles_use = int(self.candles.text())
        self.binn = int(self.bin.text())
        
        if self.coin_name.text() == "none":
            self.listcoin = [self.cb_strategy1.currentText()]
        else:
            self.listcoin = self.coin_name.text().split(',')
        # create an axis
        ax = self.figure.add_subplot(111)
        # discards the old graph
        ax.clear()
        
        for j1, coin in enumerate(self.listcoin):
            if self._exchange == "FUTURES":
                trades= self.api.futures_klines(symbol=coin, interval=self.time_interval, limit=self.candles_use)
            elif self._exchange == "SPOT":
                trades= self.api.get_klines(symbol=coin, interval=self.time_interval, limit=self.candles_use)
            
            ## candle stats
            sign = []
            for d in trades:
                if (float(d[4]) - float(d[1])):
                    sign.append(1)
                else:
                    sign.append(-1)
            percentT = [100*(float(d[2]) - float(d[3]))/float(d[2]) for i, d in enumerate(trades)]
            percentT1 = [100*sign[i]*(float(d[4]) - float(d[1]))/float(d[4]) for i, d in enumerate(trades)]
            # matplotlib histogram
            ax.hist(percentT,
                      bins = self.binn, density =True, label=coin+" Candle high-low change(%)",alpha = 0.5)
            ax.hist(percentT1,
                      bins = self.binn, density =True, label=coin+" Candle close-open change(%)",alpha = 0.5)  
            ax.axvline(np.mean(percentT), color='k', linestyle='dashed', linewidth=2)
        ax.legend(loc=4)    
        ax.set_xlabel(r'Price changes')
        ax.set_ylabel(r'Probability')
        ax.grid(linestyle='--', linewidth=0.5)
        self.canvas.draw()

class AnotherWindowDynamic(QWidget):
    def __init__(self, binance_api=None, exchange=None):
        super().__init__()
        app_icon = QtGui.QIcon()
        app_icon.addFile('logo.png', QtCore.QSize(16,16))
        self.setWindowIcon(app_icon)
        self._exchange = exchange
        self.api = binance_api
        if exchange == "FUTURES":
            info = self.api.futures_exchange_info()
        elif exchange == "SPOT":
            info = self.api.get_exchange_info()
        
        self.cb_strategy1 = QComboBox()
        for s in info['symbols']:
            self.cb_strategy1.addItem(s['symbol'])
            
        self.cb_strategy2 = QComboBox()
        self.cb_strategy2.addItem("Trades")
        if self._exchange == "FUTURES":
            self.cb_strategy2.addItem("Liquidation")

        self.candles = QLineEdit() # stop_loss_spinbox
        self.data_limit = QLineEdit() # stop_loss_spinbox
        self.interval = QLineEdit() # stop_loss_spinbox
        self.volume24 = QLineEdit() # stop_loss_spinbox
        self.volume24.setReadOnly(True)
        
        self.candles.setText("50")
        self.data_limit.setText("1000")
        self.interval.setText("1000")
        
        # button for load config file
        self.btn_config = QPushButton('Plot')
        self.btn_config.clicked.connect(self.plot_pc)
        
        self.btn_stop = QPushButton('Stop the plot')
        self.btn_stop.clicked.connect(self.plot_btn_stop)
        
        self.btn_config.setEnabled(True)
        self.btn_stop.setEnabled(False)
        
        layout = QVBoxLayout()
        # a figure instance to plot on
        # self.figure = Figure()
        # self.canvas = FigureCanvas(self.figure)
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)
             
        # set the layout
        layout.addWidget(self.toolbar, 0)
        layout.addWidget(self.canvas, 100)
        
        formLayout = QFormLayout()
        formLayout.addRow('COIN symbol (exhaustive list):', self.cb_strategy1)
        formLayout.addRow('Info to plot:', self.cb_strategy2)
        formLayout.addRow('Moving window size (in integer):', self.data_limit)
        formLayout.addRow('Nb of trades (in integer):', self.candles)
        formLayout.addRow('Plot update time (in ms integer):', self.interval)
        formLayout.addRow('24 hour volume (in USDT):', self.volume24)
        formLayout.addRow(self.btn_stop, self.btn_config)
        
        layout.addLayout(formLayout, 0)
        self.setLayout(layout)
        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        
    def plot_btn_stop(self):
        self.timer.stop()
        self.btn_config.setEnabled(True)
        self.btn_stop.setEnabled(False)
    
    def update_plot(self):
        # Drop off the first y element, append a new one.
        self.canvas.axes.cla()  # Clear the canvas.
        if self.cb_strategy2.currentText() != "Trades" and self._exchange == "FUTURES":
            self.canvas.axes.plot(self.xdata, self.ydatalb, lw=5, c='g', label=self.listcoin[0]+" Liquidation BUY (SHORTS)")
            self.canvas.axes.plot(self.xdata, self.ydatals, lw=5, c='r', label=self.listcoin[0]+" Liquidation SELL (LONGS)")
        else:
            self.canvas.axes.plot(self.xdata, self.ydata, lw=5, c='b', label=self.listcoin[0]+" (BUY-SELL)")
            self.canvas.axes.scatter(self.xdata, self.ydata1, s=10, c='g', label=self.listcoin[0]+" (BUY)")
            self.canvas.axes.scatter(self.xdata, self.ydata2, s=10, c='r', label=self.listcoin[0]+" (SELL)")
        self.canvas.axes.axhline(y=0, lw=1, c='k')
        self.canvas.axes.set_ylabel(self.listcoin[0]+' Volume in USDT)')
        # self.canvas.axes.set_xlabel(r'Time (multiple of interval)')
        self.canvas.axes.grid(linestyle='--', linewidth=0.5)
        self.canvas.axes.legend(loc=0)
        self.canvas.axes.set_xlim([self.xlinn,self.count+5])
        if self.count > 10:
            if self.cb_strategy2.currentText() != "Trades":
               self.canvas.axes.set_ylim([np.min((self.ydatalb,self.ydatals)),\
                                           np.max((self.ydatalb,self.ydatals))])
            else:
                self.canvas.axes.set_ylim([np.min((self.ydata,self.ydata1,self.ydata2)),\
                                            np.max((self.ydata,self.ydata1,self.ydata2))])
            
        self.canvas.axes1.cla()  # Clear the canvas.
        self.canvas.axes1.plot(self.xdata, self.ydata3, c='b', label=self.listcoin[0]+" price")
        self.canvas.axes1.axhline(y=0, lw=1, c='k')
        self.canvas.axes1.set_ylabel(r'Current Price')
        self.canvas.axes1.set_xlabel(r'Time (multiple of interval)')
        self.canvas.axes1.grid(linestyle='--', linewidth=0.5)
        # self.canvas.axes1.legend(loc=0,prop={'size':4})
        self.canvas.axes1.set_xlim([self.xlinn,self.count+5])
        if self.count > 10:
            self.canvas.axes1.set_ylim([np.min(self.ydata3),np.max(self.ydata3)])
        # Trigger the canvas to update and redraw.
        self.canvas.draw()
                
    def plot_pc(self):
        # self.starttime = int(time.time() * 1000)
        self.btn_config.setEnabled(False)
        self.btn_stop.setEnabled(True)
        
        self.xdata = 0
        self.ydata = 0
        self.ydata1 = 0
        self.ydata2 = 0
        self.ydata3 = 0
        self.ydatalb = 0
        self.ydatals = 0
        self.xlinn = 0

        self.candles_use = int(self.candles.text())
        self.nb_data = int(self.data_limit.text())
        self.listcoin = [self.cb_strategy1.currentText()]
        
        self.count = 0
        self.count_plt = []
        self.bms = []
        self.lb = []
        self.ls = []
        self.bmsr = []
        self.bb = []
        self.ss = []
        self.temp1 = []
        
        self.update_plot()
        
        self.timer.setInterval(int(self.interval.text()))
        self.timer.timeout.connect(self.plot_pcv1)
        self.timer.start()

    def plot_pcv1(self):
        if self._exchange == "FUTURES":
            trades= self.api.futures_recent_trades(symbol=self.listcoin[0], limit=self.candles_use)
            # TODO liquidation stream no longer possible; should start a socket for feed
            # liq = self.api.futures_liquidation_orders(symbol=self.listcoin[0], limit=self.candles_use)
            # # deal with liquidation data
            # temp_buy = [[float(d['executedQty']),float(d['price'])] for d in liq \
            #         if ([float(d['executedQty']),float(d['price'])] not in self.temp1) and (d['side']=="BUY")]
            
            # temp_sell = [[float(d['executedQty']),float(d['price'])] for d in liq \
            #         if ([float(d['executedQty']),float(d['price'])] not in self.temp1) and (d['side']=="SELL")]

            
            # for i_ in range(len(temp_buy)):
            #     self.temp1.append(temp_buy[i_])
            # for i_ in range(len(temp_sell)):
            #     self.temp1.append(temp_sell[i_])
            
            # liq_b = np.sum(np.array([t[0]*t[1] for t in temp_buy]))
            # liq_s = np.sum(np.array([t[0]*t[1] for t in temp_sell]))

            liq_b = None
            liq_s = None
        elif self._exchange == "SPOT":
            trades= self.api.get_recent_trades(symbol=self.listcoin[0], limit=self.candles_use)
            liq_b = None
            liq_s = None
             
        indices = [d['isBuyerMaker'] for d in trades]
        trades_quantity = [float(d['qty'])*float(d['price']) for d in trades] ## in USDT
        price_recent = [float(d['price']) for d in trades] ## in USDT
        indices = np.array(indices)
        trades_quantity = np.array(trades_quantity)
        price_recent = np.average(np.array(price_recent))
        
        if (self.count == 0) or (self.count%3000 == 0):
            if self._exchange == "FUTURES":
                dt = self.api.futures_ticker(symbol=self.listcoin[0])
            elif self._exchange == "SPOT":
                dt = self.api.get_ticker(symbol=self.listcoin[0])
            
            volume24 = float(dt['volume'])*float(dt['weightedAvgPrice']) ## In USDT in millions
            self.volume24.setText(str(volume24))
        
        selling = np.sum(trades_quantity[np.where(indices==True)[0]])
        buying  = np.sum(trades_quantity[np.where(indices==False)[0]])

        if self.count - self.nb_data <0:
            self.xlinn = 0
        else:
            self.xlinn = self.count - self.nb_data
            
        self.count_plt.append(self.count)
        self.bms.append(buying-selling)
        self.bb.append(buying)
        self.bmsr.append(price_recent)
        self.ss.append(selling)
        self.lb.append(liq_b)
        self.ls.append(liq_s)

        self.xdata  = self.count_plt
        self.ydata  = self.bms
        self.ydata1  = self.bb
        self.ydata2  = self.ss
        self.ydata3  = self.bmsr
        self.ydatalb  = self.lb
        self.ydatals  = self.ls
        self.update_plot()
        self.count = self.count + 1

        ## remove some data to free up RAM
        if len(self.count_plt) > 2*self.nb_data:
            self.count_plt = self.count_plt[-self.nb_data:]
            self.bms = self.bms[-self.nb_data:]
            self.bmsr = self.bmsr[-self.nb_data:]
            self.bb = self.bb[-self.nb_data:]
            self.ss = self.ss[-self.nb_data:]
            self.lb = self.lb[-self.nb_data:]
            self.ls = self.ls[-self.nb_data:]

class AnotherWindowDynamicBTC(QWidget):
    got_signal = QtCore.pyqtSignal(dict)
    
    def __init__(self, display_text=None):
        super().__init__()
        app_icon = QtGui.QIcon()
        app_icon.addFile('logo.png', QtCore.QSize(16,16))
        self.setWindowIcon(app_icon)
        
        self.display_ = display_text
        
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        
        self.cb_strategy1 = QComboBox()
        self.cb_strategy1.addItem('BTC/USD')
        self.cb_strategy1.addItem('ETH/USD')
        self.cb_strategy1.addItem('DOGE/USD')
        self.cb_strategy1.currentIndexChanged.connect(self.temp_but)
        
        self.cb_strategy2 = QComboBox()
        self.cb_strategy2.addItem("Trades")
        self.cb_strategy2.addItem("Liquidation")
        
        self.data_limit = QLineEdit() # stop_loss_spinbox
        self.interval = QLineEdit() # stop_loss_spinbox
        self.save_file = QLineEdit() # stop_loss_spinbox
        self.lots_data = QLineEdit()
        
        self.lots_data.setText("1e5,1e5,50,100,2")
        self.data_limit.setText("1000")
        self.interval.setText("1000")
        self.save_file.setText("BTC_stats")
        # button for load config file
        self.btn_config = QPushButton('Plot')
        self.btn_config.clicked.connect(self.plot_pc)
        
        self.btn_stop = QPushButton('Stop the plot')
        self.btn_stop.clicked.connect(self.plot_btn_stop)
        
        self.btn_config.setEnabled(True)
        self.btn_stop.setEnabled(False)

        self.b1 = QCheckBox("Bitmex")
        self.b1.setChecked(True)
        self.b2 = QCheckBox("Bybit")
        self.b2.setChecked(True)
        self.b3 = QCheckBox("Deribit")
        self.b3.setChecked(True)
        self.b4 = QCheckBox("Kraken")
        self.b4.setChecked(True)
        self.b5 = QCheckBox("Binance futures")
        self.b5.setChecked(True)
        self.b6 = QCheckBox("FTX futures")
        self.b6.setChecked(True)
        self.b7 = QCheckBox("Coinbase PRO")
        self.b7.setChecked(True)
        self.b8 = QCheckBox("Bitstamp")
        self.b8.setChecked(True)
        self.b9 = QCheckBox("Binance")
        self.b9.setChecked(True)
        self.b10 = QCheckBox("FTX")
        self.b10.setChecked(True)
        
        layout = QVBoxLayout()
        # a figure instance to plot on
        # self.figure = Figure()
        # self.canvas = FigureCanvas(self.figure)
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)
             
        # set the layout
        layout.addWidget(self.toolbar, 0)
        layout.addWidget(self.canvas, 100)
        
        formLayout = QFormLayout()
        formLayout.addRow('COIN symbol (Multiple exchanges):', self.cb_strategy1)
        formLayout.addRow(self.b1, self.b2)
        formLayout.addRow(self.b3, self.b4)
        formLayout.addRow(self.b5, self.b6)
        formLayout.addRow(self.b7, self.b8)
        formLayout.addRow(self.b9, self.b10)
        formLayout.addRow('Info to plot:', self.cb_strategy2)
        formLayout.addRow('Moving window size (in integer):', self.data_limit)
        formLayout.addRow('Plot update time (in ms integer):', self.interval)
        formLayout.addRow('Threshold, investment, safety, trades for LONG/SHORT:', self.lots_data)
        formLayout.addRow('save file:', self.save_file)
        formLayout.addRow(self.btn_stop, self.btn_config)
        
        layout.addLayout(formLayout, 0)
        
        self.setLayout(layout)
        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer12 = QtCore.QTimer()
    
    def temp_but(self):
        if self.cb_strategy1.currentText() == 'DOGE/USD':
            self.b2.setEnabled(False)
            self.b2.setChecked(False)
            self.b3.setEnabled(False)
            self.b3.setChecked(False)
            self.b4.setEnabled(False)
            self.b4.setChecked(False)
            self.b7.setEnabled(False)
            self.b7.setChecked(False)
            self.b8.setEnabled(False)
            self.b8.setChecked(False)
        else:
            self.b1.setEnabled(True)
            self.b2.setEnabled(True)
            self.b3.setEnabled(True)
            self.b4.setEnabled(True)
            self.b7.setEnabled(True)
            self.b8.setEnabled(True)
            self.b5.setEnabled(True)
            self.b6.setEnabled(True)
            self.b9.setEnabled(True)
            self.b10.setEnabled(True)
        
    def closeEvent(self, event):
        try:
            self.driver.close()
            self.driver.quit()
        except:
            pass
        self.timer12.stop()
        self.close()
        
    def plot_btn_stop(self):
        try:
            self.driver.close()
            self.driver.quit()
        except:
            pass
        self.timer12.stop()
        self.btn_config.setEnabled(True)
        self.cb_strategy1.setEnabled(True)
        self.btn_stop.setEnabled(False)
        
        self.b1.setEnabled(True)
        self.b2.setEnabled(True)
        self.b3.setEnabled(True)
        self.b4.setEnabled(True)
        self.b7.setEnabled(True)
        self.b8.setEnabled(True)
        self.b5.setEnabled(True)
        self.b6.setEnabled(True)
        self.b9.setEnabled(True)
        self.b10.setEnabled(True)
    
    def update_plot(self):
        # Drop off the first y element, append a new one.
        self.canvas.axes.cla()  # Clear the canvas.
        if self.cb_strategy2.currentText() == 'Trades':
            self.canvas.axes.plot(self.xdata, self.ydata, lw=5, c='b', label="(BUY-SELL)")
            self.canvas.axes.scatter(self.xdata, self.ydata1, s=10, c='g', label="(BUY)")
            self.canvas.axes.scatter(self.xdata, self.ydata2, s=10, c='r', label="(SELL)")
        elif self.cb_strategy2.currentText() == 'Liquidation':
            self.canvas.axes.plot(self.xdata, self.ydatalb, lw=5, c='g', label="Liquidation BUY (SHORTS)")
            self.canvas.axes.plot(self.xdata, self.ydatals, lw=5, c='r', label="Liquidation SELL (LONGS)")
        self.canvas.axes.axhline(y=0, lw=1, c='k')
        self.canvas.axes.set_ylabel(r'Volume in USDT')
        self.canvas.axes.grid(linestyle='--', linewidth=0.5)
        self.canvas.axes.legend(loc=0)
        self.canvas.axes.set_xlim([self.xlinn,self.count+5])
        if self.count > 10:
            if self.cb_strategy2.currentText() == 'Trades':
                self.canvas.axes.set_ylim([np.min((self.ydata,self.ydata1,self.ydata2)),\
                                            np.max((self.ydata,self.ydata1,self.ydata2))])
            else:
                self.canvas.axes.set_ylim([np.min((self.ydatalb,self.ydatals)),\
                                           np.max((self.ydatalb,self.ydatals))])
            
        self.canvas.axes1.cla()  # Clear the canvas.
        self.canvas.axes1.plot(self.xdata, self.ydata3, lw=5, c='b')
        self.canvas.axes1.axhline(y=0, lw=1, c='k')
        self.canvas.axes1.set_ylabel(r'Current Weighted Price')
        self.canvas.axes1.set_xlabel(r'Time (multiples of interval)')
        self.canvas.axes1.grid(linestyle='--', linewidth=0.5)
        self.canvas.axes1.set_xlim([self.xlinn,self.count+5])
        if self.count > 10:
            self.canvas.axes1.set_ylim([np.min(self.ydata3),np.max(self.ydata3)])
        # Trigger the canvas to update and redraw.
        self.canvas.draw()
                
    def plot_pc(self):
        
        # try:        
        url='https://coinlobster.com/combined.html'
        flag = 0x08000000  # No-Window flag
        webdriver.common.service.subprocess.Popen = functools.partial(
                                                    webdriver.common.service.subprocess.Popen, 
                                                    creationflags=flag)
        self.driver = webdriver.Firefox(options=self.options)
        self.driver.get(url)
        time.sleep(5) ## allows to load page
        # except:
        #     return
        
        self.b1.setEnabled(False)
        self.b2.setEnabled(False)
        self.b3.setEnabled(False)
        self.b4.setEnabled(False)
        self.b5.setEnabled(False)
        self.b6.setEnabled(False)
        self.b7.setEnabled(False)
        self.b8.setEnabled(False)
        self.b9.setEnabled(False)
        self.b10.setEnabled(False)
        
        self.btn_config.setEnabled(False)
        self.cb_strategy1.setEnabled(False)
        self.btn_stop.setEnabled(True)
        
        select = self.driver.find_element_by_id('selected-pair-option')
        select.click()
        time.sleep(2)
        coin_consider = self.cb_strategy1.currentText()
        a = select.parent.find_elements_by_tag_name('a')
        time.sleep(2)
        if coin_consider == 'BTC/USD':
            a[21].click() # FOR BTC/USD
            self.save_file.setText("BTC_stats")
        elif coin_consider == 'ETH/USD':
            a[22].click() # FOR ETH/USD
            self.save_file.setText("ETH_stats")
        elif coin_consider == 'DOGE/USD':
            a[23].click()
            self.save_file.setText("DOGE_stats")
        
        time.sleep(2)
        
        select1 = self.driver.find_element_by_id('futures-exchanges-list')
        i = select1.parent.find_elements_by_tag_name('i')
        
        if coin_consider == 'BTC/USD' or coin_consider == 'ETH/USD':
            if self.b1.isChecked() == False:
                i[8].click() #BITMEX DOGE
            if self.b2.isChecked() == False:
                i[9].click() # BYBIT
            if self.b3.isChecked() == False:
                i[10].click() # DERIBIT
            if self.b4.isChecked() == False:
                i[11].click() # Kraken futures
            if self.b5.isChecked() == False:
                i[12].click() # Binance futures DOGE
            if self.b6.isChecked() == False:
                i[13].click() # Ftx futures DOGE
            if self.b7.isChecked() == False:
                i[14].click() # Coinbase PRO
            if self.b8.isChecked() == False:
                i[15].click() # Bitstamp
            if self.b9.isChecked() == False:
                i[16].click() # Binance DOGE
            if self.b10.isChecked() == False:
                i[17].click() # Ftx DOGE
            ## save some ram
            i[19].click() # Close plots
            i[20].click() # Close Piechart
            i[21].click() # Close Weighted average price
            i[7].click() ## market list
        elif coin_consider == 'DOGE/USD':
            if self.b1.isChecked() == False:
                i[8].click() #BITMEX DOGE
            if self.b5.isChecked() == False:
                i[9].click() # Binance futures DOGE
            if self.b6.isChecked() == False:
                i[10].click() # Ftx futures DOGE
            if self.b9.isChecked() == False:
                i[11].click() # Binance DOGE
            if self.b10.isChecked() == False:
                i[12].click() # Ftx DOGE
            ## save some ram
            i[15].click() # Close plots
            i[16].click() # Close Piechart
            i[17].click() # Close Weighted average price
            i[7].click() ## market list
        ct = time.time()
        now = datetime.datetime.fromtimestamp(ct)
        c_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename_ = self.save_file.text() + "_" + c_time
        self.save_file.setText(filename_)
        
        exc = ['binance', 'binancefutures', 'bitmex', 'bitstamp', 'bybit',
               'coinbasepro', 'deribit', 'ftx', 'ftxfutures', 'krakenfutures']
        
        str1 = [i+"_BTC_bought" for i in exc]
        str2 = [i+"_BTC_sold" for i in exc]
        str3 = [i+"_liquidations_(LONGS)" for i in exc]
        str4 = [i+"_liquidations_(SHORTS)" for i in exc]
        
        str1 = ' '.join(str1)
        str2 = ' '.join(str2)
        str3 = ' '.join(str3)
        str4 = ' '.join(str4)
        big_string = " " + str1 + " " + str2 + " " + str3 + " " + str4 + " \n"
        with open(self.save_file.text()+".txt", "w") as myfile:
            myfile.write("#Date_Time BTC_average_price(USDT) BTC_bought(USDT) BTC_sold(USDT)"+\
                         " Total_liquidations_(SHORTS) Total_liquidations_(LONGS)"+big_string)
        
        self.xdata = 0
        self.ydata = 0
        self.ydata1 = 0
        self.ydata2 = 0
        self.ydata3 = 0
        self.xlinn = 0
        self.ydatalb = 0
        self.ydatals = 0
        
        self.nb_data = int(self.data_limit.text())
        
        self.count = 0
        self.count_plt = []
        self.bms = []
        self.bmsr = []
        self.bb = []
        self.ss = []
        self.lb = []
        self.ls = []
        self.temp1 = []
        
        self.update_plot()
        
        self.timer12.setInterval(int(self.interval.text()))
        self.timer12.timeout.connect(self.plot_pcv1)
        self.timer12.start()

    def plot_pcv1(self):
        
        #↕ split the content of the liq details
        tempp = self.lots_data.text()
        tempp = tempp.split(',')
        
        content = self.driver.page_source
        soup = BeautifulSoup(content, features="html.parser")

        ## Get the whole table (doing trades only)
        trades = soup.find('tbody', {'id':"trades"})
        table_tr_sell = trades.find_all('tr', {"class": "trade-detail text-danger"})
        data_sold = []
        exchange_sold = []
        for row in table_tr_sell:
            img = row.find('img')
            exchange_sold.append(img['src'].split('/')[-1].split('.')[0].split('-')[0])
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            temp = [float(ele.replace(',','')) for ele in cols[:2] if ele] #:2 to not consider time
            data_sold.append(temp[0] * temp[1]) # Get rid of empty values
            
        table_tr_buy = trades.find_all('tr', {"class": "trade-detail text-success"})    
        data_buy = []
        exchange_buy = []
        for row in table_tr_buy:
            img = row.find('img')
            exchange_buy.append(img['src'].split('/')[-1].split('.')[0].split('-')[0])
            cols = row.find_all('td')
            cols = [ele.text.strip()  for ele in cols]
            temp = [float(ele.replace(',','')) for ele in cols[:2] if ele] #:2 to not consider time
            data_buy.append(temp[0] * temp[1]) # Get rid of empty values
        data_buy = np.array(data_buy)
        data_sold = np.array(data_sold)
        
        selling = np.sum(data_sold)
        buying  = np.sum(data_buy)
        # orderbook = soup.find('tbody', {'id':"orderbook"})
        # table_ob = orderbook.find_all('tr')
        
        liquidations = soup.find('tbody', {'id':"liquidations"})   
        ## LONGS GETTING LIQUIDATED
        liquidations_sell = liquidations.find_all('tr', {"class": "liquidation-detail text-danger"})
        exchange_red = []
        data_red = []
        for row in liquidations_sell:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            temp = [float(ele.replace(',','')) for ele in cols[:2] if ele] #:2 to not consider time
            if temp in self.temp1:
                continue
            else:
                img = row.find('img')
                exchange_red.append(img['src'].split('/')[-1].split('.')[0].split('-')[0])
                self.temp1.append(temp)
            data_red.append(temp[0] * temp[1]) # Get rid of empty values
        ## SHORTS GETTING LIQUIDATED
        liquidations_buy = liquidations.find_all('tr', {"class": "liquidation-detail text-success"})  
        exchange_green = []
        data_green = []
        for row in liquidations_buy:
            cols = row.find_all('td')
            cols = [ele.text.strip()  for ele in cols]
            temp = [float(ele.replace(',','')) for ele in cols[:2] if ele] #:2 to not consider time
            if temp in self.temp1:
                continue
            else:
                img = row.find('img')
                exchange_green.append(img['src'].split('/')[-1].split('.')[0].split('-')[0])
                self.temp1.append(temp)
            data_green.append(temp[0] * temp[1]) # Get rid of empty values
        data_green = np.array(data_green)
        data_red = np.array(data_red)
        
        liq_red = np.sum(data_red)
        liq_green  = np.sum(data_green)
        
        # TODO (Preliminary version)
        #### make a filter here and send signal via dict to the Qmainwindow for the bot
        #### to change strategy based on the BTC dynamic
        emit_dictionary = False
        if liq_red > float(tempp[0]) and self.count > 20:
            emit_dictionary = {"direction": "SHORT", "investment": float(tempp[2]), \
                               "safety": float(tempp[3]), "limtrades":int(tempp[4])}
        if liq_green > float(tempp[1]) and self.count > 20:
            emit_dictionary = {"direction": "LONG", "investment": float(tempp[2]), \
                               "safety": float(tempp[3]), "limtrades":int(tempp[4])}
        if emit_dictionary:
            self.got_signal.emit(emit_dictionary)
        
        recent_price = soup.find('h1', {'id':"weighted-mid"})
        price_recent = float(recent_price.text.strip().replace(',',''))
        
        ## sort based on exchanges
        exc = ['binance', 'binancefutures', 'bitmex', 'bitstamp', 'bybit',
               'coinbasepro', 'deribit', 'ftx', 'ftxfutures', 'krakenfutures']
        list_exc_sold = [[] for i in range(len(exc))]
        list_exc_buy = [[] for i in range(len(exc))]
        list_exc_red = [[] for i in range(len(exc))]
        list_exc_green = [[] for i in range(len(exc))]
        for ind_, exe_ in enumerate(exc):
            list_exc_sold[ind_].append(np.sum(data_sold[np.where(np.array(exchange_sold)==exe_)[0]]))
            list_exc_buy[ind_].append(np.sum(data_buy[np.where(np.array(exchange_buy)==exe_)[0]]))
            if len(data_red) > 0:
                list_exc_red[ind_].append(np.sum(data_red[np.where(np.array(exchange_red)==exe_)[0]]))
            if len(data_green) > 0:
                list_exc_green[ind_].append(np.sum(data_green[np.where(np.array(exchange_green)==exe_)[0]]))
        
        str1 = [str(round(i[0],0)) for i in list_exc_sold]
        str2 = [str(round(i[0],0)) for i in list_exc_buy]
        str3 = []
        for i in list_exc_red:
            if len(i) > 0:
                str3.append(str(round(i[0],0)))
            else:
                str3.append(str(0))
                
        str4 = []
        for i in list_exc_green:
            if len(i) > 0:
                str4.append(str(round(i[0],0)))
            else:
                str4.append(str(0))        
        
        str1 = ' '.join(str1)
        str2 = ' '.join(str2)
        str3 = ' '.join(str3)
        str4 = ' '.join(str4)
        big_string = " " + str1 + " " + str2 + " " + str3 + " " + str4 + " \n"
        ct = time.time()
        now = datetime.datetime.fromtimestamp(ct)
        c_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        with open(self.save_file.text()+".txt", "a") as myfile:
            myfile.write(c_time+ " "+str(round(price_recent, 0))+" "+ str(round(buying, 0)) +\
                         " "+ str(round(selling,0))+" "+ str(round(liq_green,0))+\
                             " "+ str(round(liq_red,0))+ big_string)

        if (self.count - self.nb_data) < 0:
            self.xlinn = 0
        else:
            self.xlinn = self.count - self.nb_data
        
        self.count_plt.append(self.count)
        self.bms.append(buying-selling)
        self.bb.append(buying)
        self.bmsr.append(price_recent)
        self.ss.append(selling)
        self.lb.append(liq_green)
        self.ls.append(liq_red)
        
        self.xdata  = self.count_plt
        self.ydata  = self.bms
        self.ydata1  = self.bb
        self.ydata2  = self.ss
        self.ydata3  = self.bmsr
        self.ydatalb  = self.lb
        self.ydatals  = self.ls
        self.update_plot()
        
        self.count = self.count + 1
        
        ## remove some data to free up RAM
        if len(self.count_plt) > 2*self.nb_data:
            # ind_tem = len(self.temp1)//2
            # self.temp1 = self.temp1[-ind_tem:]
            self.count_plt = self.count_plt[-self.nb_data:]
            self.bms = self.bms[-self.nb_data:]
            self.bmsr = self.bmsr[-self.nb_data:]
            self.bb = self.bb[-self.nb_data:]
            self.ss = self.ss[-self.nb_data:]
            self.lb = self.lb[-self.nb_data:]
            self.ls = self.ls[-self.nb_data:]

class AnotherWindowDynamicFS(QWidget):
    got_text = QtCore.pyqtSignal(dict)
    def __init__(self, binance_api=None):
        super().__init__()
        app_icon = QtGui.QIcon()
        app_icon.addFile('logo.png', QtCore.QSize(16,16))
        self.setWindowIcon(app_icon)
        self.counting = 0
        self.api = binance_api
        info = self.api.futures_exchange_info()
        
        self.coins = []
        self.cb_strategy1 = QComboBox()
        for s in info['symbols']:
            self.coins.append(s['symbol'])
            self.cb_strategy1.addItem(s['symbol'])

        self.progress = QProgressBar()
        # self.progress.setGeometry(0, 0, 300, 25)
        self.progress.setMaximum(len(self.coins))
        
        self.interval = QComboBox()
        for s in ["5m","15m","30m","1h","2h","4h","6h","12h","1d"]:
            self.interval.addItem(s)
        self.interval.setCurrentText("15m") 
         
        self.candles = QLineEdit() # stop_loss_spinbox
        self.candles.setText("10")
        # button for load config file
        self.btn_config = QPushButton('Plot')
        self.btn_config.clicked.connect(self.plot_pc)
        
        self.btn_config1 = QPushButton('Print stats (takes time)')
        self.btn_config1.clicked.connect(self.plot_pc1)
        
        layout = QVBoxLayout()
        # a figure instance to plot on
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100, subplot=1)
        self.toolbar = NavigationToolbar(self.canvas, self)
        # set the layout
        layout.addWidget(self.toolbar, 0)
        layout.addWidget(self.canvas, 100)
        formLayout = QFormLayout()
        formLayout.addRow('COIN symbol (exhaustive list):', self.cb_strategy1)
        formLayout.addRow('Nb of trades (in integer MAX 30):', self.candles)
        formLayout.addRow('Data update time:', self.interval)
        formLayout.addRow(self.btn_config1, self.btn_config)
        formLayout.addRow(self.progress)
        layout.addLayout(formLayout, 0)
        self.setLayout(layout)
        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer3 = QtCore.QTimer()
        self.start = 0
        
    def update_plot(self):
        # Drop off the first y element, append a new one.
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(self.xdata, self.ydata, lw=5, c='r', ls="dashed", label="top_LongShortAccountRatio")
        self.canvas.axes.plot(self.xdata2, self.ydata2, lw=5, c='r', label="global_LongShortAccountRatio")
        self.canvas.axes.plot(self.xdata1, self.ydata1, lw=5, c='g', label="top_LongShortPositionRatio")
        self.canvas.axes.scatter(self.xdata3, self.ydata3, s=50, c='b', label="buy_sell_volume_ratio")
        self.canvas.axes.axhline(y=0, lw=1, c='k')
        self.canvas.axes.set_ylabel(self.listcoin[0])
        # self.canvas.axes.set_xlabel(r'Time (multiple of interval)')
        self.canvas.axes.grid(linestyle='--', linewidth=0.5)
        self.canvas.axes.legend(loc=0)
        # self.canvas.axes.set_xticklabels(self.xdata, rotation=90)
        self.canvas.axes.tick_params(axis='x', labelrotation=90)
        # self.canvas.axes.set_ylim([np.min((self.ydata,self.ydata1,self.ydata2,self.ydata3)),\
        #                                     np.max((self.ydata,self.ydata1,self.ydata2,self.ydata3))])
        # Trigger the canvas to update and redraw.
        self.canvas.draw()
        
    def qsd(self):
        self.progress.setValue(self.counting)
        if self.start == 1:
            self.timer3.stop()
            
    def temp_print(self,):
        self.start = 0
        emit_dictionary = {}
        emit_dictionary['coin'] = []
        emit_dictionary['TimeFrame'] = []
        emit_dictionary['topLongShortAccountRatio'] = []
        emit_dictionary['topLongShortPositionRatio'] = []
        emit_dictionary['globalLongShortAccountRatio'] = []
        emit_dictionary['takerlongshortRatio'] = []
        count = 0
        for s in self.coins:
            trades1 = self.api.futures_topLongShortAccountRatio(symbol=s,
                                                                period=self.interval.currentText(),
                                                                limit=1)
            trades2 = self.api.futures_topLongShortPositionRatio(symbol=s,
                                                                 period=self.interval.currentText(),
                                                                 limit=1)
            trades3 = self.api.futures_globalLongShortAccountRatio(symbol=s,
                                                                   period=self.interval.currentText(),
                                                                   limit=1)
            trades4 = self.api.futures_takerlongshortRatio(symbol=s,
                                                           period=self.interval.currentText(),
                                                           limit=1)
            ### get order book data
            long_short_ratio1 = np.array([float(d['longShortRatio']) for d in trades1]) ## in CRYPTO
            long_short_ratio2 = np.array([float(d['longShortRatio']) for d in trades2]) ## in CRYPTO
            long_short_ratio3 = np.array([float(d['longShortRatio']) for d in trades3]) ## in CRYPTO
            buy_sell_ratio = np.array([float(d['buySellRatio']) for d in trades4]) ## in CRYPTO
            emit_dictionary['coin'].append(s)
            emit_dictionary['TimeFrame'].append(self.interval.currentText())
            emit_dictionary['topLongShortAccountRatio'].append(long_short_ratio1)
            emit_dictionary['topLongShortPositionRatio'].append(long_short_ratio2)
            emit_dictionary['globalLongShortAccountRatio'].append(long_short_ratio3)
            emit_dictionary['takerlongshortRatio'].append(buy_sell_ratio)
            count = count + 1
            self.counting = count
        self.got_text.emit(emit_dictionary)
        self.btn_config1.setEnabled(True)
        self.btn_config.setEnabled(True)
        self.start = 1
    
    def plot_pc1(self):
        self.btn_config.setEnabled(False)
        self.btn_config1.setEnabled(False)
        # self.temp_print()
        self.timer3.setInterval(1000)
        self.timer3.timeout.connect(self.qsd)
        self.timer3.start()
        temp_ = threading.Thread(target=self.temp_print, daemon=False)
        temp_.start()
            
    def plot_pc(self):
        self.btn_config.setEnabled(False)
        candles_use = int(self.candles.text())
        self.listcoin = [self.cb_strategy1.currentText()]
        trades1 = self.api.futures_topLongShortAccountRatio(symbol=self.listcoin[0],
                                                            period=self.interval.currentText(),
                                                            limit=candles_use)
        trades2 = self.api.futures_topLongShortPositionRatio(symbol=self.listcoin[0],
                                                             period=self.interval.currentText(),
                                                             limit=candles_use)
        trades3 = self.api.futures_globalLongShortAccountRatio(symbol=self.listcoin[0],
                                                               period=self.interval.currentText(),
                                                               limit=candles_use)
        trades4 = self.api.futures_takerlongshortRatio(symbol=self.listcoin[0],
                                                       period=self.interval.currentText(),
                                                       limit=candles_use)
        ### get order book data
        long_short_ratio1 = np.array([float(d['longShortRatio']) for d in trades1]) ## in CRYPTO
        long_short_ratio2 = np.array([float(d['longShortRatio']) for d in trades2]) ## in CRYPTO
        long_short_ratio3 = np.array([float(d['longShortRatio']) for d in trades3]) ## in CRYPTO
        buy_sell_ratio = np.array([float(d['buySellRatio']) for d in trades4]) ## in CRYPTO
        
        long_short_ratio1ts = np.array([float(d['timestamp']) for d in trades1]) ## in CRYPTO
        long_short_ratio2ts = np.array([float(d['timestamp']) for d in trades2]) ## in CRYPTO
        long_short_ratio3ts = np.array([float(d['timestamp']) for d in trades3]) ## in CRYPTO
        buy_sell_ratiots = np.array([float(d['timestamp']) for d in trades4])
        
        date_x = []
        for i in range(len(long_short_ratio1ts)):
            date = datetime.datetime.fromtimestamp(long_short_ratio1ts[i] / 1e3)
            date_x.append(date.strftime("%Y-%m-%d %H-%M"))
        date_x1 = []
        for i in range(len(long_short_ratio2ts)):
            date = datetime.datetime.fromtimestamp(long_short_ratio2ts[i] / 1e3)
            date_x1.append(date.strftime("%Y-%m-%d %H-%M"))
        date_x2 = []
        for i in range(len(long_short_ratio3ts)):
            date = datetime.datetime.fromtimestamp(long_short_ratio3ts[i] / 1e3)
            date_x2.append(date.strftime("%Y-%m-%d %H-%M"))
        date_x3 = []
        for i in range(len(buy_sell_ratiots)):
            date = datetime.datetime.fromtimestamp(buy_sell_ratiots[i] / 1e3)
            date_x3.append(date.strftime("%Y-%m-%d %H-%M"))
            
        self.xdata  = date_x
        self.xdata1  = date_x1
        self.xdata2  = date_x2
        self.xdata3  = date_x3
        self.ydata  = long_short_ratio1
        self.ydata1  = long_short_ratio2
        self.ydata2  = long_short_ratio3
        self.ydata3  = buy_sell_ratio
        self.update_plot()
        self.btn_config.setEnabled(True)

class AnotherWindowConfig(QWidget):#QWidget QScrollArea
    got_password = QtCore.pyqtSignal(dict)
    
    def __init__(self, binance_api=None, state=0):
        super().__init__()
        
        app_icon = QtGui.QIcon()
        app_icon.addFile('logo.png', QtCore.QSize(16,16))
        self.setWindowIcon(app_icon)
        self.settings = QSettings("config_data","ConfigGUI")
        
        if binance_api == None:
            self.api = None
        else:
            self.api = binance_api

        # Binance module        
        self.enablebinance = QComboBox()
        self.enablebinance.addItem("True")
        self.enablebinance.addItem("False")
        self.keybinance = QLineEdit("binancekey") #
        self.secretbinance = QLineEdit("binancesecret") #
        self.keybinance.setText("")
        self.secretbinance.setText("")
        # Telegram module
        self.enabletelegram = QComboBox()
        self.enabletelegram.addItem("True")
        self.enabletelegram.addItem("False")  
        self.botToken = QLineEdit("telegrambottoken") # 
        self.botchatid = QLineEdit("telegrambotid") #         
        self.botToken.setText("")
        self.botchatid.setText("")
        
        # Live trade module (coins and blacklist)
        self.enabletrade = QComboBox()
        self.enabletrade.addItem("True")
        self.enabletrade.addItem("False")
        
        self.coinsinit = QLineEdit("coins") # 
        self.blacklist = QLineEdit("blacklist") # 
        self.coinsinit.setText("all")
        self.blacklist.setText("BTCSTUSDT")
        
        self.cb_priceanalysis = QComboBox()
        self.cb_priceanalysis.addItem("market")
        self.cb_priceanalysis.addItem("last_price")
        self.cb_priceanalysis.addItem("bid")
        self.cb_priceanalysis.addItem("ask")
        self.cb_priceanalysis.addItem("bid_ask")
        self.cb_priceanalysis.addItem("liquidation")

        self.cb_strategy1 = QLineEdit("candle")
        self.cb_strategy1.setText("300")
        self.cb_strategy2 = QLineEdit("candleinterval")
        self.cb_strategy2.setText("2")
        # order data
        self.investment = QLineEdit("investment") # stop_loss_spinbox
        self.leverage = QLineEdit("leverage") # stop_loss_spinbox
        self.addfunds = QLineEdit("addfunds") # stop_loss_spinbox
        self.investment.setText("50")
        self.leverage.setText("9")
        self.addfunds.setText("100")
        
        self.limtrade = QLineEdit("limtrades") # auto_sell_spinbox
        self.safetypercent = QLineEdit("safetydrop") # stop_loss_spinbox
        self.limtradecoin = QLineEdit("percoinlimtrades") # stop_loss_spinbox
        self.profit = QLineEdit("profit") # stop_loss_spinbox
        self.trailing = QLineEdit("ttp") # stop_loss_spinbox
        self.limtrade.setText("3")
        self.safetypercent.setText("3.0")
        self.limtradecoin.setText("3")
        self.profit.setText("1.1")
        self.trailing.setText("0.2")
        
        self.enableprofit = QComboBox()
        self.enableprofit.addItem("True")
        self.enableprofit.addItem("False")
        
        self.is_exchange_market = True
        self.cb_exchange = QComboBox()
        self.cb_exchange.addItem("Binance Futures")
        self.cb_exchange.addItem("Binance Spot")
        self.cb_exchange.currentIndexChanged.connect(self.selectionchange_exchange)
        
        self.cb_mode = QComboBox()
        self.cb_mode.addItem("Manual")
        self.cb_mode.addItem("Automatic")
        
        self.is_order_market = True
        self.cb_strategy = QComboBox()
        self.cb_strategy.addItem("LONG")
        self.cb_strategy.addItem("SHORT")
        self.cb_strategy.currentIndexChanged.connect(self.selectionchange_strategy)
        
        self.cb_strategybase = QComboBox()
        self.cb_strategybase.addItem("USDT")
        self.cb_strategybase.addItem("BTC")
        self.cb_strategybase.addItem("BNB")
        self.cb_strategybase.addItem("ETH")
        self.cb_strategybase.addItem("USD")
        self.cb_strategybase.addItem("EUR")
        
        # button for load config file
        self.btn_config = QPushButton('Apply new settings')
        self.btn_config.clicked.connect(self.read_config_dynamic)
        close_button = QPushButton("Cancel")
        close_button.clicked.connect(self.close)

        self.layout = QVBoxLayout() # QGridLayout()

        formLayout = QFormLayout()
        # formLayout.setVerticalSpacing(5)
        formLayout.addRow('BINANCE SETTINGS', QLineEdit().setReadOnly(True))
        formLayout.addRow('Exchange type:', self.cb_exchange)
        formLayout.addRow('Order strategy:', self.cb_strategy)
        formLayout.addRow('Base Currency:', self.cb_strategybase)
        formLayout.addRow('Enable BINANCE:', self.enablebinance)
        formLayout.addRow('BINANCE key:', self.keybinance)
        formLayout.addRow('BINANCE secret:', self.secretbinance)
        # formLayout.setVerticalSpacing(5)
        formLayout.addRow('TELEGRAM SETTINGS', QLineEdit().setReadOnly(True))
        formLayout.addRow('Enable Telegram:', self.enabletelegram)
        formLayout.addRow('Telegram bot token:', self.botToken)
        formLayout.addRow('Telegram chat id:', self.botchatid)
        # formLayout.setVerticalSpacing(5)
        formLayout.addRow('TRADE SETTINGS', QLineEdit().setReadOnly(True))
        formLayout.addRow('Live trade:', self.enabletrade)
        formLayout.addRow('Coins to trade:', self.coinsinit)
        formLayout.addRow('Blacklist:', self.blacklist)
        formLayout.addRow('Price analysis method:', self.cb_priceanalysis)
        formLayout.addRow('Time to analyze (in sec):', self.cb_strategy1)
        formLayout.addRow('Time interval (in sec):', self.cb_strategy2)
        formLayout.addRow('Maximum allowed trades (per account):', self.limtrade)
        formLayout.addRow('Maximum allowed trades (per coin for safety):', self.limtradecoin)
        # formLayout.setVerticalSpacing(5)
        formLayout.addRow('Trade mode:', self.cb_mode)
        formLayout.addRow('PROFIT SETTINGS',QLineEdit().setReadOnly(True))
        formLayout.addRow('Take profit:', self.enableprofit)
        formLayout.addRow('Closing profit (in %):', self.profit)
        formLayout.addRow('Trailing profit (in  %):', self.trailing)
        # formLayout.setVerticalSpacing(5)
        formLayout.addRow('ORDER SETTINGS',QLineEdit().setReadOnly(True))
        formLayout.addRow('Initial Investment (USDT):', self.investment)
        formLayout.addRow('Add funds (safety in USDT):', self.addfunds)
        formLayout.addRow('Safety drops (%):', self.safetypercent)
        formLayout.addRow('Leverage to use:', self.leverage)
        # formLayout.setVerticalSpacing(5)
        formLayout.addRow(close_button, self.btn_config)

        self.layout.addLayout(formLayout)
        self.setLayout(self.layout)

        if state > 0:
            self._gui_restore()

    def _gui_save(self):
      # Save geometry
        for name, obj in inspect.getmembers(self):
          # if type(obj) is QComboBox:  # this works similar to isinstance, but missed some field... not sure why?
          if isinstance(obj, QComboBox):
              index = obj.currentIndex()  # get current index from combobox
              text = obj.itemText(index)  # get the text for current index
              self.settings.setValue(name, text)  # save combobox selection to registry
          if isinstance(obj, QLineEdit):
              value = obj.text()
              self.settings.setValue(name, value)  # save ui values, so they can be restored next time
        self.settings.sync()
        
    def _gui_restore(self):
        # Restore geometry  
        for name, obj in inspect.getmembers(self):
            if isinstance(obj, QComboBox):
                index = obj.currentIndex()  # get current region from combobox
                value = (self.settings.value(name))
                if value == "":
                    continue
                index = obj.findText(value)  # get the corresponding index for specified string in combobox
          
                if index == -1:  # add to list if not found
                      obj.insertItems(0, [value])
                      index = obj.findText(value)
                      obj.setCurrentIndex(index)
                else:
                      obj.setCurrentIndex(index)  # preselect a combobox value by index
            if isinstance(obj, QLineEdit):
                value = (self.settings.value(name))#.decode('utf-8'))  # get stored value from registry
                obj.setText(value)  # restore lineEditFile
        self.settings.sync()
    
    def selectionchange_exchange(self,i):        		
        if self.cb_exchange.currentText() == "Binance Futures":
            self.is_exchange_market = True
        elif self.cb_exchange.currentText() == "Binance Spot":
            self.is_exchange_market = False

    def selectionchange_strategy(self, i):
        if self.cb_strategy.currentText() == "LONG":
            self.is_order_market = True
        elif self.cb_strategy.currentText() == "SHORT":
            self.is_order_market = False 
    
    def read_config_dynamic(self):
        self._gui_save()
        
        self.text1 = []
        
        self.basecurrency = self.cb_strategybase.currentText()
        
        candlesP = int(self.cb_strategy1.text())
        interval = int(self.cb_strategy2.text())
        self.candlesP = [int(i) for i in range(1, candlesP, interval)]

        if self.api == None:
            if self.enablebinance.currentText() == "True":
                bin_key = self.keybinance.text()
                bin_secret = self.secretbinance.text()
                self.api = Client(bin_key, bin_secret) #futures_income_history
            elif self.enablebinance.currentText() == "False":
                bin_key = self.keybinance.text()
                bin_secret = self.secretbinance.text()
                self.api = None
        else:
            bin_key = self.keybinance.text()
            bin_secret = self.secretbinance.text()
            
        if self.enabletelegram.currentText() == "True":
            self.enabledT = True
        elif self.enabletelegram.currentText() == "False":
            self.enabledT = False
                
        if self.enabletrade.currentText() == "True":
            self.live_trade = True
        elif self.enabletrade.currentText() == "False":
            self.live_trade = False
            
        if self.enableprofit.currentText() == "True":
            self.take_profit = "true"
        elif self.enableprofit.currentText() == "False":
            self.take_profit = "false"

        self.bot_chatID = self.botchatid.text()
        self.bot_token = self.botToken.text()
        self.lim_trades = int(self.limtrade.text())

        self.profit_percent = float(self.profit.text())
        self.take_profit_trailing = float(self.trailing.text())
        self.safety_trade_percent = float(self.safetypercent.text())
        self.usdt_addfunds = float(self.addfunds.text())
        self.usdt_invest = float(self.investment.text())
        self.leverage = int(self.leverage.text())
        
        ## get all list of coins in Binance futures:
        if self.is_exchange_market:
            info = self.api.futures_exchange_info()
        else:
            info = self.api.get_exchange_info()
        
        all_coins =  [x['symbol'] for x in info['symbols'] if x['symbol'][-len(self.basecurrency):] == self.basecurrency]
        
        self.lim_trades_per_coin = {}
        self.trade_per_coin = {}
        for i in all_coins:
            self.lim_trades_per_coin[i] = int(self.limtradecoin.text())
            self.trade_per_coin[i] = int(0)
            
        if self.take_profit_trailing > 0.0:
            self.ttp = 'true'
        else:
            self.ttp = 'false'

        ## verify how many coins are provided
        if 'all' in self.coinsinit.text():
            self.coins = all_coins
        else:
            self.coins = [i for i in self.coinsinit.text().split(',')]
        ## verify how many coins are blacklisted    
        black_list = self.blacklist.text().split(",")
        if 'none' in black_list:
            self.black_list = ['none']
        else:
            self.black_list = [i for i in black_list]
            msg = ''
            for i in self.black_list:
                msg = msg + '; '+i
            self.text1.append("The following pair(s) are backlisted: "+msg)
            
        msg = ''
        for i in self.coins:
            if i in self.black_list:
                continue
            msg = msg + ', '+i
            
        self.text1.append("The following pair(s) (with base currency of "+self.basecurrency+\
                          ") will be traded (provided their volume is above given threshold) "+msg)
        if not 'none' in self.black_list:
            for i in self.black_list:
                if i in self.coins:
                    self.coins.remove(i)
        self.text1.append("Bot configuration loaded successfully")

        # create a dictionary and emit the signal
        emit_dictionary = {"binance_client": self.api,
                            "binance_key": bin_key,
                            "binance_secret": bin_secret,
                            "text1": self.text1,
                            "enabledT": self.enabledT,
                            "live_trade": self.live_trade,
                            "take_profit": self.take_profit,
                            "bot_chatID": self.bot_chatID,
                            "bot_token": self.bot_token,
                            "ttp": self.ttp,
                            "lim_trades": self.lim_trades,
                            "profit_percent": self.profit_percent,
                            "take_profit_trailing": self.take_profit_trailing,
                            "safety_trade_percent": self.safety_trade_percent,
                            "usdt_addfunds": self.usdt_addfunds,
                            "usdt_invest": self.usdt_invest,
                            "leverage": self.leverage,
                            "lim_trades_per_coin": self.lim_trades_per_coin,
                            "trade_per_coin": self.trade_per_coin,
                            "coins": self.coins,
                            "black_list": self.black_list,
                            "price_analysis_mode": self.cb_priceanalysis.currentText(),
                            "candlesP": self.candlesP,
                            "is_exchange_market": self.is_exchange_market,
                            "is_order_market": self.is_order_market,
                            "basecurrency": self.basecurrency,
                            "mode_analysis": self.cb_mode.currentText()}
        self.got_password.emit(emit_dictionary)
        self.close() # close the window
        
class Client(object):
    API_URL = 'https://api.binance.{}/api'
    WITHDRAW_API_URL = 'https://api.binance.{}/wapi'
    MARGIN_API_URL = 'https://api.binance.{}/sapi'
    WEBSITE_URL = 'https://www.binance.{}'
    FUTURES_URL = 'https://fapi.binance.{}/fapi'
    FUTURES_DATA_URL = 'https://fapi.binance.{}/futures/data'
    FUTURES_COIN_URL = "https://dapi.binance.{}/dapi"
    FUTURES_COIN_DATA_URL = "https://dapi.binance.{}/futures/data"
    OPTIONS_URL = 'https://vapi.binance.{}/vapi'
    OPTIONS_TESTNET_URL = 'https://testnet.binanceops.{}/vapi'
    PUBLIC_API_VERSION = 'v1'
    PRIVATE_API_VERSION = 'v3'
    WITHDRAW_API_VERSION = 'v3'
    MARGIN_API_VERSION = 'v1'
    FUTURES_API_VERSION = 'v1'
    FUTURES_API_VERSION2 = "v2"
    OPTIONS_API_VERSION = 'v1'

    SYMBOL_TYPE_SPOT = 'SPOT'

    ORDER_STATUS_NEW = 'NEW'
    ORDER_STATUS_PARTIALLY_FILLED = 'PARTIALLY_FILLED'
    ORDER_STATUS_FILLED = 'FILLED'
    ORDER_STATUS_CANCELED = 'CANCELED'
    ORDER_STATUS_PENDING_CANCEL = 'PENDING_CANCEL'
    ORDER_STATUS_REJECTED = 'REJECTED'
    ORDER_STATUS_EXPIRED = 'EXPIRED'

    KLINE_INTERVAL_1MINUTE = '1m'
    KLINE_INTERVAL_3MINUTE = '3m'
    KLINE_INTERVAL_5MINUTE = '5m'
    KLINE_INTERVAL_15MINUTE = '15m'
    KLINE_INTERVAL_30MINUTE = '30m'
    KLINE_INTERVAL_1HOUR = '1h'
    KLINE_INTERVAL_2HOUR = '2h'
    KLINE_INTERVAL_4HOUR = '4h'
    KLINE_INTERVAL_6HOUR = '6h'
    KLINE_INTERVAL_8HOUR = '8h'
    KLINE_INTERVAL_12HOUR = '12h'
    KLINE_INTERVAL_1DAY = '1d'
    KLINE_INTERVAL_3DAY = '3d'
    KLINE_INTERVAL_1WEEK = '1w'
    KLINE_INTERVAL_1MONTH = '1M'

    SIDE_BUY = 'BUY'
    SIDE_SELL = 'SELL'

    ORDER_TYPE_LIMIT = 'LIMIT'
    ORDER_TYPE_MARKET = 'MARKET'
    ORDER_TYPE_STOP_LOSS = 'STOP_LOSS'
    ORDER_TYPE_STOP_LOSS_LIMIT = 'STOP_LOSS_LIMIT'
    ORDER_TYPE_TAKE_PROFIT = 'TAKE_PROFIT'
    ORDER_TYPE_TAKE_PROFIT_LIMIT = 'TAKE_PROFIT_LIMIT'
    ORDER_TYPE_LIMIT_MAKER = 'LIMIT_MAKER'

    FUTURE_ORDER_TYPE_LIMIT = 'LIMIT'
    FUTURE_ORDER_TYPE_MARKET = 'MARKET'
    FUTURE_ORDER_TYPE_STOP = 'STOP'
    FUTURE_ORDER_TYPE_STOP_MARKET = 'STOP_MARKET'
    FUTURE_ORDER_TYPE_TAKE_PROFIT = 'TAKE_PROFIT'
    FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET = 'TAKE_PROFIT_MARKET'
    FUTURE_ORDER_TYPE_LIMIT_MAKER = 'LIMIT_MAKER'
	
    TIME_IN_FORCE_GTC = 'GTC'  # Good till cancelled
    TIME_IN_FORCE_IOC = 'IOC'  # Immediate or cancel
    TIME_IN_FORCE_FOK = 'FOK'  # Fill or kill

    ORDER_RESP_TYPE_ACK = 'ACK'
    ORDER_RESP_TYPE_RESULT = 'RESULT'
    ORDER_RESP_TYPE_FULL = 'FULL'

    # For accessing the data returned by Client.aggregate_trades().
    AGG_ID = 'a'
    AGG_PRICE = 'p'
    AGG_QUANTITY = 'q'
    AGG_FIRST_TRADE_ID = 'f'
    AGG_LAST_TRADE_ID = 'l'
    AGG_TIME = 'T'
    AGG_BUYER_MAKES = 'm'
    AGG_BEST_MATCH = 'M'

    # new asset transfer api enum
    SPOT_TO_FIAT = "MAIN_C2C"
    SPOT_TO_USDT_FUTURE = "MAIN_UMFUTURE"
    SPOT_TO_COIN_FUTURE = "MAIN_CMFUTURE"
    SPOT_TO_MARGIN_CROSS = "MAIN_MARGIN"
    SPOT_TO_MINING = "MAIN_MINING"
    FIAT_TO_SPOT = "C2C_MAIN"
    FIAT_TO_USDT_FUTURE = "C2C_UMFUTURE"
    FIAT_TO_MINING = "C2C_MINING"
    USDT_FUTURE_TO_SPOT = "UMFUTURE_MAIN"
    USDT_FUTURE_TO_FIAT = "UMFUTURE_C2C"
    USDT_FUTURE_TO_MARGIN_CROSS = "UMFUTURE_MARGIN"
    COIN_FUTURE_TO_SPOT = "CMFUTURE_MAIN"
    MARGIN_CROSS_TO_SPOT = "MARGIN_MAIN"
    MARGIN_CROSS_TO_USDT_FUTURE = "MARGIN_UMFUTURE"
    MINING_TO_SPOT = "MINING_MAIN"
    MINING_TO_USDT_FUTURE = "MINING_UMFUTURE"
    MINING_TO_FIAT = "MINING_C2C"

    def __init__(self, api_key=None, api_secret=None, requests_params=None, tld='com', testnet=False):
        """Binance API Client constructor

        :param api_key: Api Key
        :type api_key: str.
        :param api_secret: Api Secret
        :type api_secret: str.
        :param requests_params: optional - Dictionary of requests params to use for all calls
        :type requests_params: dict.
        :param testnet: Use testnet environment - only available for vanilla options at the moment
        :type testnet: bool

        """

        self.API_URL = self.API_URL.format(tld)
        self.WITHDRAW_API_URL = self.WITHDRAW_API_URL.format(tld)
        self.MARGIN_API_URL = self.MARGIN_API_URL.format(tld)
        self.WEBSITE_URL = self.WEBSITE_URL.format(tld)
        self.FUTURES_URL = self.FUTURES_URL.format(tld)
        self.FUTURES_DATA_URL = self.FUTURES_DATA_URL.format(tld)
        self.FUTURES_COIN_URL = self.FUTURES_COIN_URL.format(tld)
        self.FUTURES_COIN_DATA_URL = self.FUTURES_COIN_DATA_URL.format(tld)
        self.OPTIONS_URL = self.OPTIONS_URL.format(tld)
        self.OPTIONS_TESTNET_URL = self.OPTIONS_TESTNET_URL.format(tld)

        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.session = self._init_session()
        self._requests_params = requests_params
        self.response = None
        self.testnet = testnet
        self.timestamp_offset = 0

        # init DNS and SSL cert
        self.ping()
        # calculate timestamp offset between local and binance server
        res = self.get_server_time()
        self.timestamp_offset = res['serverTime'] - int(time.time() * 1000)

    def _init_session(self):

        session = requests.session()
        session.headers.update({'Accept': 'application/json',
                                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                                'X-MBX-APIKEY': self.API_KEY})
        return session

    def _create_api_uri(self, path, signed=True, version=PUBLIC_API_VERSION):
        v = self.PRIVATE_API_VERSION if signed else version
        return self.API_URL + '/' + v + '/' + path

    def _create_withdraw_api_uri(self, path):
        return self.WITHDRAW_API_URL + '/' + self.WITHDRAW_API_VERSION + '/' + path

    def _create_margin_api_uri(self, path):
        return self.MARGIN_API_URL + '/' + self.MARGIN_API_VERSION + '/' + path

    def _create_website_uri(self, path):
        return self.WEBSITE_URL + '/' + path

    def _create_futures_api_uri(self, path, version=1):
        options = {1: self.FUTURES_API_VERSION, 2: self.FUTURES_API_VERSION2}
        return self.FUTURES_URL + "/" + options[version] + "/" + path
        # return self.FUTURES_URL + '/' + self.FUTURES_API_VERSION + '/' + path

    def _create_futures_data_api_uri(self, path):
        return self.FUTURES_DATA_URL + '/' + path

    def _create_futures_coin_api_url(self, path, version=1):
        options = {1: self.FUTURES_API_VERSION, 2: self.FUTURES_API_VERSION2}
        return self.FUTURES_COIN_URL + "/" + options[version] + "/" + path

    def _create_futures_coin_data_api_url(self, path, version=1):
        return self.FUTURES_COIN_DATA_URL + "/" + path

    def _create_options_api_uri(self, path):
        if self.testnet:
            url =  self.OPTIONS_TESTNET_URL
        else:
            url = self.OPTIONS_URL
        return url + '/' + self.OPTIONS_API_VERSION + '/' + path

    def _generate_signature(self, data):

        ordered_data = self._order_params(data)
        query_string = '&'.join(["{}={}".format(d[0], d[1]) for d in ordered_data])
        m = hmac.new(self.API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256)
        return m.hexdigest()

    def _order_params(self, data):
        """Convert params to list with signature as last element

        :param data:
        :return:

        """
        has_signature = False
        params = []
        for key, value in data.items():
            if key == 'signature':
                has_signature = True
            else:
                params.append((key, value))
        # sort parameters by key
        params.sort(key=itemgetter(0))
        if has_signature:
            params.append(('signature', data['signature']))
        return params

    def _request(self, method, uri, signed, force_params=False, **kwargs):

        # set default requests timeout
        kwargs['timeout'] = 10

        # add our global requests params
        if self._requests_params:
            kwargs.update(self._requests_params)

        data = kwargs.get('data', None)
        if data and isinstance(data, dict):
            kwargs['data'] = data

            # find any requests params passed and apply them
            if 'requests_params' in kwargs['data']:
                # merge requests params into kwargs
                kwargs.update(kwargs['data']['requests_params'])
                del(kwargs['data']['requests_params'])

        if signed:
            # generate signature
            kwargs['data']['timestamp'] = int(time.time() * 1000 + self.timestamp_offset)
            kwargs['data']['signature'] = self._generate_signature(kwargs['data'])

        # sort get and post params to match signature order
        if data:
            # sort post params
            kwargs['data'] = self._order_params(kwargs['data'])
            # Remove any arguments with values of None.
            null_args = [i for i, (key, value) in enumerate(kwargs['data']) if value is None]
            for i in reversed(null_args):
                del kwargs['data'][i]

        # if get request assign data array to params value for requests lib
        if data and (method == 'get' or force_params):
            kwargs['params'] = '&'.join('%s=%s' % (data[0], data[1]) for data in kwargs['data'])
            del(kwargs['data'])

        self.response = getattr(self.session, method)(uri, **kwargs)
        return self._handle_response()

    def _request_api(self, method, path, signed=False, version=PUBLIC_API_VERSION, **kwargs):
        uri = self._create_api_uri(path, signed, version)

        return self._request(method, uri, signed, **kwargs)

    def _request_withdraw_api(self, method, path, signed=False, **kwargs):
        uri = self._create_withdraw_api_uri(path)

        return self._request(method, uri, signed, True, **kwargs)

    def _request_margin_api(self, method, path, signed=False, **kwargs):
        uri = self._create_margin_api_uri(path)

        return self._request(method, uri, signed, **kwargs)

    def _request_website(self, method, path, signed=False, **kwargs):
        uri = self._create_website_uri(path)

        return self._request(method, uri, signed, **kwargs)

    def _request_futures_api(self, method, path, signed=False, version=1, **kwargs):
        uri = self._create_futures_api_uri(path, version)

        return self._request(method, uri, signed, True, **kwargs)

    def _request_futures_data_api(self, method, path, signed=False, **kwargs):
        uri = self._create_futures_data_api_uri(path)

        return self._request(method, uri, signed, True, **kwargs)

    def _request_futures_coin_api(self, method, path, signed=False, version=1, **kwargs):
        uri = self._create_futures_coin_api_url(path, version=version)

        return self._request(method, uri, signed, True, **kwargs)

    def _request_futures_coin_data_api(self, method, path, signed=False, version=1, **kwargs):
        uri = self._create_futures_coin_data_api_url(path, version=version)

        return self._request(method, uri, signed, True, **kwargs)

    def _request_options_api(self, method, path, signed=False, **kwargs):
        uri = self._create_options_api_uri(path)

        return self._request(method, uri, signed, True, **kwargs)

    def _handle_response(self):
        """Internal helper for handling API responses from the Binance server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """
        if not (200 <= self.response.status_code < 300):
            raise BinanceAPIException(self.response)
        try:
            return self.response.json()
        except ValueError:
            raise BinanceRequestException('Invalid Response: %s' % self.response.text)

    def _get(self, path, signed=False, version=PUBLIC_API_VERSION, **kwargs):
        return self._request_api('get', path, signed, version, **kwargs)

    def _post(self, path, signed=False, version=PUBLIC_API_VERSION, **kwargs):
        return self._request_api('post', path, signed, version, **kwargs)

    def _put(self, path, signed=False, version=PUBLIC_API_VERSION, **kwargs):
        return self._request_api('put', path, signed, version, **kwargs)

    def _delete(self, path, signed=False, version=PUBLIC_API_VERSION, **kwargs):
        return self._request_api('delete', path, signed, version, **kwargs)

    # Exchange Endpoints

    def get_products(self):
        """Return list of products currently listed on Binance

        Use get_exchange_info() call instead

        :returns: list - List of product dictionaries

        :raises: BinanceRequestException, BinanceAPIException

        """
        products = self._request_website('get', 'exchange-api/v1/public/asset-service/product/get-products')
        return products

    def get_exchange_info(self):
        """Return rate limits and list of symbols

        :returns: list - List of product dictionaries

        .. code-block:: python

            {
                "timezone": "UTC",
                "serverTime": 1508631584636,
                "rateLimits": [
                    {
                        "rateLimitType": "REQUESTS",
                        "interval": "MINUTE",
                        "limit": 1200
                    },
                    {
                        "rateLimitType": "ORDERS",
                        "interval": "SECOND",
                        "limit": 10
                    },
                    {
                        "rateLimitType": "ORDERS",
                        "interval": "DAY",
                        "limit": 100000
                    }
                ],
                "exchangeFilters": [],
                "symbols": [
                    {
                        "symbol": "ETHBTC",
                        "status": "TRADING",
                        "baseAsset": "ETH",
                        "baseAssetPrecision": 8,
                        "quoteAsset": "BTC",
                        "quotePrecision": 8,
                        "orderTypes": ["LIMIT", "MARKET"],
                        "icebergAllowed": false,
                        "filters": [
                            {
                                "filterType": "PRICE_FILTER",
                                "minPrice": "0.00000100",
                                "maxPrice": "100000.00000000",
                                "tickSize": "0.00000100"
                            }, {
                                "filterType": "LOT_SIZE",
                                "minQty": "0.00100000",
                                "maxQty": "100000.00000000",
                                "stepSize": "0.00100000"
                            }, {
                                "filterType": "MIN_NOTIONAL",
                                "minNotional": "0.00100000"
                            }
                        ]
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """

        return self._get('exchangeInfo', version=self.PRIVATE_API_VERSION)

    def get_symbol_info(self, symbol):
        """Return information about a symbol

        :param symbol: required e.g BNBBTC
        :type symbol: str

        :returns: Dict if found, None if not

        .. code-block:: python

            {
                "symbol": "ETHBTC",
                "status": "TRADING",
                "baseAsset": "ETH",
                "baseAssetPrecision": 8,
                "quoteAsset": "BTC",
                "quotePrecision": 8,
                "orderTypes": ["LIMIT", "MARKET"],
                "icebergAllowed": false,
                "filters": [
                    {
                        "filterType": "PRICE_FILTER",
                        "minPrice": "0.00000100",
                        "maxPrice": "100000.00000000",
                        "tickSize": "0.00000100"
                    }, {
                        "filterType": "LOT_SIZE",
                        "minQty": "0.00100000",
                        "maxQty": "100000.00000000",
                        "stepSize": "0.00100000"
                    }, {
                        "filterType": "MIN_NOTIONAL",
                        "minNotional": "0.00100000"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """

        res = self._get('exchangeInfo', version=self.PRIVATE_API_VERSION)

        for item in res['symbols']:
            if item['symbol'] == symbol.upper():
                return item

        return None

    # General Endpoints

    def ping(self):
        """Test connectivity to the Rest API.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#test-connectivity

        :returns: Empty array

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('ping', version=self.PRIVATE_API_VERSION)

    def get_server_time(self):
        """Test connectivity to the Rest API and get the current server time.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#check-server-time

        :returns: Current server time

        .. code-block:: python

            {
                "serverTime": 1499827319559
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('time', version=self.PRIVATE_API_VERSION)

    # Market Data Endpoints

    def get_all_tickers(self):
        """Latest price for all symbols.

        https://www.binance.com/restapipub.html#symbols-price-ticker

        :returns: List of market tickers

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "price": "4.00000200"
                },
                {
                    "symbol": "ETHBTC",
                    "price": "0.07946600"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('ticker/price', version=self.PRIVATE_API_VERSION)

    def get_orderbook_tickers(self):
        """Best price/qty on the order book for all symbols.

        https://www.binance.com/restapipub.html#symbols-order-book-ticker

        :returns: List of order book market entries

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "bidPrice": "4.00000000",
                    "bidQty": "431.00000000",
                    "askPrice": "4.00000200",
                    "askQty": "9.00000000"
                },
                {
                    "symbol": "ETHBTC",
                    "bidPrice": "0.07946700",
                    "bidQty": "9.00000000",
                    "askPrice": "100000.00000000",
                    "askQty": "1000.00000000"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('ticker/bookTicker', version=self.PRIVATE_API_VERSION)

    def get_order_book(self, **params):
        """Get the Order Book for the market

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#order-book

        :param symbol: required
        :type symbol: str
        :param limit:  Default 100; max 1000
        :type limit: int

        :returns: API response

        .. code-block:: python

            {
                "lastUpdateId": 1027024,
                "bids": [
                    [
                        "4.00000000",     # PRICE
                        "431.00000000",   # QTY
                        []                # Can be ignored
                    ]
                ],
                "asks": [
                    [
                        "4.00000200",
                        "12.00000000",
                        []
                    ]
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('depth', data=params, version=self.PRIVATE_API_VERSION)

    def get_recent_trades(self, **params):
        """Get recent trades (up to last 500).

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#recent-trades-list

        :param symbol: required
        :type symbol: str
        :param limit:  Default 500; max 500.
        :type limit: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "id": 28457,
                    "price": "4.00000100",
                    "qty": "12.00000000",
                    "time": 1499865549590,
                    "isBuyerMaker": true,
                    "isBestMatch": true
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('trades', data=params)

    def get_historical_trades(self, **params):
        """Get older trades.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#recent-trades-list

        :param symbol: required
        :type symbol: str
        :param limit:  Default 500; max 500.
        :type limit: int
        :param fromId:  TradeId to fetch from. Default gets most recent trades.
        :type fromId: str

        :returns: API response

        .. code-block:: python

            [
                {
                    "id": 28457,
                    "price": "4.00000100",
                    "qty": "12.00000000",
                    "time": 1499865549590,
                    "isBuyerMaker": true,
                    "isBestMatch": true
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('historicalTrades', data=params, version=self.PRIVATE_API_VERSION)

    def get_aggregate_trades(self, **params):
        """Get compressed, aggregate trades. Trades that fill at the time,
        from the same order, with the same price will have the quantity aggregated.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#compressedaggregate-trades-list

        :param symbol: required
        :type symbol: str
        :param fromId:  ID to get aggregate trades from INCLUSIVE.
        :type fromId: str
        :param startTime: Timestamp in ms to get aggregate trades from INCLUSIVE.
        :type startTime: int
        :param endTime: Timestamp in ms to get aggregate trades until INCLUSIVE.
        :type endTime: int
        :param limit:  Default 500; max 500.
        :type limit: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "a": 26129,         # Aggregate tradeId
                    "p": "0.01633102",  # Price
                    "q": "4.70443515",  # Quantity
                    "f": 27781,         # First tradeId
                    "l": 27781,         # Last tradeId
                    "T": 1498793709153, # Timestamp
                    "m": true,          # Was the buyer the maker?
                    "M": true           # Was the trade the best price match?
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('aggTrades', data=params, version=self.PRIVATE_API_VERSION)

    # def aggregate_trade_iter(self, symbol, start_str=None, last_id=None):
    #     """Iterate over aggregate trade data from (start_time or last_id) to
    #     the end of the history so far.

    #     If start_time is specified, start with the first trade after
    #     start_time. Meant to initialise a local cache of trade data.

    #     If last_id is specified, start with the trade after it. This is meant
    #     for updating a pre-existing local trade data cache.

    #     Only allows start_str or last_id—not both. Not guaranteed to work
    #     right if you're running more than one of these simultaneously. You
    #     will probably hit your rate limit.

    #     See dateparser docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/

    #     If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

    #     :param symbol: Symbol string e.g. ETHBTC
    #     :type symbol: str
    #     :param start_str: Start date string in UTC format or timestamp in milliseconds. The iterator will
    #     return the first trade occurring later than this time.
    #     :type start_str: str|int
    #     :param last_id: aggregate trade ID of the last known aggregate trade.
    #     Not a regular trade ID. See https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#compressedaggregate-trades-list.

    #     :returns: an iterator of JSON objects, one per trade. The format of
    #     each object is identical to Client.aggregate_trades().

    #     :type last_id: int
    #     """
    #     if start_str is not None and last_id is not None:
    #         raise ValueError(
    #             'start_time and last_id may not be simultaneously specified.')

    #     # If there's no last_id, get one.
    #     if last_id is None:
    #         # Without a last_id, we actually need the first trade.  Normally,
    #         # we'd get rid of it. See the next loop.
    #         if start_str is None:
    #             trades = self.get_aggregate_trades(symbol=symbol, fromId=0)
    #         else:
    #             # The difference between startTime and endTime should be less
    #             # or equal than an hour and the result set should contain at
    #             # least one trade.
    #             if type(start_str) == int:
    #                 start_ts = start_str
    #             else:
    #                 start_ts = date_to_milliseconds(start_str)
    #             # If the resulting set is empty (i.e. no trades in that interval)
    #             # then we just move forward hour by hour until we find at least one
    #             # trade or reach present moment
    #             while True:
    #                 end_ts = start_ts + (60 * 60 * 1000)
    #                 trades = self.get_aggregate_trades(
    #                     symbol=symbol,
    #                     startTime=start_ts,
    #                     endTime=end_ts)
    #                 if len(trades) > 0:
    #                     break
    #                 # If we reach present moment and find no trades then there is
    #                 # nothing to iterate, so we're done
    #                 if end_ts > int(time.time() * 1000):
    #                     return
    #                 start_ts = end_ts
    #         for t in trades:
    #             yield t
    #         last_id = trades[-1][self.AGG_ID]

    #     while True:
    #         # There is no need to wait between queries, to avoid hitting the
    #         # rate limit. We're using blocking IO, and as long as we're the
    #         # only thread running calls like this, Binance will automatically
    #         # add the right delay time on their end, forcing us to wait for
    #         # data. That really simplifies this function's job. Binance is
    #         # fucking awesome.
    #         trades = self.get_aggregate_trades(symbol=symbol, fromId=last_id)
    #         # fromId=n returns a set starting with id n, but we already have
    #         # that one. So get rid of the first item in the result set.
    #         trades = trades[1:]
    #         if len(trades) == 0:
    #             return
    #         for t in trades:
    #             yield t
    #         last_id = trades[-1][self.AGG_ID]

    def get_klines(self, **params):
        """Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#klinecandlestick-data

        :param symbol: required
        :type symbol: str
        :param interval: -
        :type interval: str
        :param limit: - Default 500; max 500.
        :type limit: int
        :param startTime:
        :type startTime: int
        :param endTime:
        :type endTime: int

        :returns: API response

        .. code-block:: python

            [
                [
                    1499040000000,      # Open time
                    "0.01634790",       # Open
                    "0.80000000",       # High
                    "0.01575800",       # Low
                    "0.01577100",       # Close
                    "148976.11427815",  # Volume
                    1499644799999,      # Close time
                    "2434.19055334",    # Quote asset volume
                    308,                # Number of trades
                    "1756.87402397",    # Taker buy base asset volume
                    "28.46694368",      # Taker buy quote asset volume
                    "17928899.62484339" # Can be ignored
                ]
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('klines', data=params, version=self.PRIVATE_API_VERSION)

    def _klines(self, spot=True, **params):
        """Get klines of spot (get_klines) or futures (futures_klines) endpoints.

        :param spot: Spot klines functions, otherwise futures
        :type spot: bool

        :return: klines, see get_klines

        """
        if spot:
            return self.get_klines(**params)
        else:
            return self.futures_klines(**params)

    def _get_earliest_valid_timestamp(self, symbol, interval, spot):
        """Get earliest valid open timestamp from Binance

        :param symbol: Name of symbol pair e.g BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param spot: Spot endpoint, otherwise futures
        :type spot: bool

        :return: first valid timestamp

        """
        kline = self._klines(spot=spot,
                             symbol=symbol,
                             interval=interval,
                             limit=1,
                             startTime=0,
                             endTime=None
                             )
        return kline[0][0]

    def get_historical_klines(self, symbol, interval, start_str, end_str=None,
                           limit=500):
        """Get Historical Klines from Binance

        :param symbol: Name of symbol pair e.g BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param start_str: Start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: str|int
        :param limit: Default 500; max 1000.
        :type limit: int

        :return: list of OHLCV values

        """
        return self._historical_klines(symbol, interval, start_str, end_str=None, limit=500, spot=True)

    # def _historical_klines(self, symbol, interval, start_str, end_str=None,
    #                        limit=500, spot=True):
    #     """Get Historical Klines from Binance (spot or futures)

    #     See dateparser docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/

    #     If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

    #     :param symbol: Name of symbol pair e.g BNBBTC
    #     :type symbol: str
    #     :param interval: Binance Kline interval
    #     :type interval: str
    #     :param start_str: Start date string in UTC format or timestamp in milliseconds
    #     :type start_str: str|int
    #     :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
    #     :type end_str: str|int
    #     :param limit: Default 500; max 1000.
    #     :type limit: int
    #     :param limit: Default 500; max 1000.
    #     :type limit: int
    #     :param spot: Historical klines from spot endpoint, otherwise futures
    #     :type spot: bool

    #     :return: list of OHLCV values

    #     """
    #     # init our list
    #     output_data = []

    #     # setup the max limit
    #     limit = limit

    #     # convert interval to useful value in seconds
    #     timeframe = interval_to_milliseconds(interval)

    #     # convert our date strings to milliseconds
    #     if type(start_str) == int:
    #         start_ts = start_str
    #     else:
    #         start_ts = date_to_milliseconds(start_str)

    #     # establish first available start timestamp
    #     first_valid_ts = self._get_earliest_valid_timestamp(symbol, interval, spot)
    #     start_ts = max(start_ts, first_valid_ts)

    #     # if an end time was passed convert it
    #     end_ts = None
    #     if end_str:
    #         if type(end_str) == int:
    #             end_ts = end_str
    #         else:
    #             end_ts = date_to_milliseconds(end_str)

    #     idx = 0
    #     while True:
    #         # fetch the klines from start_ts up to max 500 entries or the end_ts if set
    #         temp_data = self._klines(
    #             spot=spot,
    #             symbol=symbol,
    #             interval=interval,
    #             limit=limit,
    #             startTime=start_ts,
    #             endTime=end_ts
    #         )

    #         # handle the case where exactly the limit amount of data was returned last loop
    #         if not len(temp_data):
    #             break

    #         # append this loops data to our output data
    #         output_data += temp_data

    #         # set our start timestamp using the last value in the array
    #         start_ts = temp_data[-1][0]

    #         idx += 1
    #         # check if we received less than the required limit and exit the loop
    #         if len(temp_data) < limit:
    #             # exit the while loop
    #             break

    #         # increment next call by our timeframe
    #         start_ts += timeframe

    #         # sleep after every 3rd call to be kind to the API
    #         if idx % 3 == 0:
    #             time.sleep(1)

    #     return output_data

    def get_historical_klines_generator(self, symbol, interval, start_str, end_str=None):
        """Get Historical Klines generator from Binance

        :param symbol: Name of symbol pair e.g BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param start_str: Start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: str|int

        :return: generator of OHLCV values

        """

        return self._historical_klines_generator(symbol, interval, start_str, end_str=end_str, spot=True)

    # def _historical_klines_generator(self, symbol, interval, start_str, end_str=None, spot=True):
    #     """Get Historical Klines generator from Binance (spot or futures)

    #     See dateparser docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/

    #     If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

    #     :param symbol: Name of symbol pair e.g BNBBTC
    #     :type symbol: str
    #     :param interval: Binance Kline interval
    #     :type interval: str
    #     :param start_str: Start date string in UTC format or timestamp in milliseconds
    #     :type start_str: str|int
    #     :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
    #     :type end_str: str|int
    #     :param spot: Historical klines generator from spot endpoint, otherwise futures
    #     :type spot: bool

    #     :return: generator of OHLCV values

    #     """

    #     # setup the max limit
    #     limit = 500

    #     # convert interval to useful value in seconds
    #     timeframe = interval_to_milliseconds(interval)

    #     # convert our date strings to milliseconds
    #     if type(start_str) == int:
    #         start_ts = start_str
    #     else:
    #         start_ts = date_to_milliseconds(start_str)

    #     # establish first available start timestamp
    #     first_valid_ts = self._get_earliest_valid_timestamp(symbol, interval, spot)
    #     start_ts = max(start_ts, first_valid_ts)

    #     # if an end time was passed convert it
    #     end_ts = None
    #     if end_str:
    #         if type(end_str) == int:
    #             end_ts = end_str
    #         else:
    #             end_ts = date_to_milliseconds(end_str)

    #     idx = 0
    #     while True:
    #         # fetch the klines from start_ts up to max 500 entries or the end_ts if set
    #         output_data = self.get_klines(
    #             spot=spot,
    #             symbol=symbol,
    #             interval=interval,
    #             limit=limit,
    #             startTime=start_ts,
    #             endTime=end_ts
    #         )

    #         # handle the case where exactly the limit amount of data was returned last loop
    #         if not len(output_data):
    #             break

    #         # yield data
    #         for o in output_data:
    #             yield o

    #         # set our start timestamp using the last value in the array
    #         start_ts = output_data[-1][0]

    #         idx += 1
    #         # check if we received less than the required limit and exit the loop
    #         if len(output_data) < limit:
    #             # exit the while loop
    #             break

    #         # increment next call by our timeframe
    #         start_ts += timeframe

    #         # sleep after every 3rd call to be kind to the API
    #         if idx % 3 == 0:
    #             time.sleep(1)

    def get_avg_price(self, **params):
        """Current average price for a symbol.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#current-average-price

        :param symbol:
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "mins": 5,
                "price": "9.35751834"
            }
        """
        return self._get('avgPrice', data=params, version=self.PRIVATE_API_VERSION)

    def get_ticker(self, **params):
        """24 hour price change statistics.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#24hr-ticker-price-change-statistics

        :param symbol:
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "priceChange": "-94.99999800",
                "priceChangePercent": "-95.960",
                "weightedAvgPrice": "0.29628482",
                "prevClosePrice": "0.10002000",
                "lastPrice": "4.00000200",
                "bidPrice": "4.00000000",
                "askPrice": "4.00000200",
                "openPrice": "99.00000000",
                "highPrice": "100.00000000",
                "lowPrice": "0.10000000",
                "volume": "8913.30000000",
                "openTime": 1499783499040,
                "closeTime": 1499869899040,
                "fristId": 28385,   # First tradeId
                "lastId": 28460,    # Last tradeId
                "count": 76         # Trade count
            }

        OR

        .. code-block:: python

            [
                {
                    "priceChange": "-94.99999800",
                    "priceChangePercent": "-95.960",
                    "weightedAvgPrice": "0.29628482",
                    "prevClosePrice": "0.10002000",
                    "lastPrice": "4.00000200",
                    "bidPrice": "4.00000000",
                    "askPrice": "4.00000200",
                    "openPrice": "99.00000000",
                    "highPrice": "100.00000000",
                    "lowPrice": "0.10000000",
                    "volume": "8913.30000000",
                    "openTime": 1499783499040,
                    "closeTime": 1499869899040,
                    "fristId": 28385,   # First tradeId
                    "lastId": 28460,    # Last tradeId
                    "count": 76         # Trade count
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('ticker/24hr', data=params, version=self.PRIVATE_API_VERSION)

    def get_symbol_ticker(self, **params):
        """Latest price for a symbol or symbols.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#24hr-ticker-price-change-statistics

        :param symbol:
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "symbol": "LTCBTC",
                "price": "4.00000200"
            }

        OR

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "price": "4.00000200"
                },
                {
                    "symbol": "ETHBTC",
                    "price": "0.07946600"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('ticker/price', data=params, version=self.PRIVATE_API_VERSION)

    def get_orderbook_ticker(self, **params):
        """Latest price for a symbol or symbols.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#symbol-order-book-ticker

        :param symbol:
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "symbol": "LTCBTC",
                "bidPrice": "4.00000000",
                "bidQty": "431.00000000",
                "askPrice": "4.00000200",
                "askQty": "9.00000000"
            }

        OR

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "bidPrice": "4.00000000",
                    "bidQty": "431.00000000",
                    "askPrice": "4.00000200",
                    "askQty": "9.00000000"
                },
                {
                    "symbol": "ETHBTC",
                    "bidPrice": "0.07946700",
                    "bidQty": "9.00000000",
                    "askPrice": "100000.00000000",
                    "askQty": "1000.00000000"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('ticker/bookTicker', data=params, version=self.PRIVATE_API_VERSION)

    # Account Endpoints

    def create_order(self, **params):
        """Send in a new order

        Any order with an icebergQty MUST have timeInForce set to GTC.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#new-order--trade

        :param symbol: required
        :type symbol: str
        :param side: required
        :type side: str
        :param type: required
        :type type: str
        :param timeInForce: required if limit order
        :type timeInForce: str
        :param quantity: required
        :type quantity: decimal
        :param quoteOrderQty: amount the user wants to spend (when buying) or receive (when selling)
            of the quote asset, applicable to MARKET orders
        :type quoteOrderQty: decimal
        :param price: required
        :type price: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param icebergQty: Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        Response ACK:

        .. code-block:: python

            {
                "symbol":"LTCBTC",
                "orderId": 1,
                "clientOrderId": "myOrder1" # Will be newClientOrderId
                "transactTime": 1499827319559
            }

        Response RESULT:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595,
                "price": "0.00000000",
                "origQty": "10.00000000",
                "executedQty": "10.00000000",
                "status": "FILLED",
                "timeInForce": "GTC",
                "type": "MARKET",
                "side": "SELL"
            }

        Response FULL:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595,
                "price": "0.00000000",
                "origQty": "10.00000000",
                "executedQty": "10.00000000",
                "status": "FILLED",
                "timeInForce": "GTC",
                "type": "MARKET",
                "side": "SELL",
                "fills": [
                    {
                        "price": "4000.00000000",
                        "qty": "1.00000000",
                        "commission": "4.00000000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3999.00000000",
                        "qty": "5.00000000",
                        "commission": "19.99500000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3998.00000000",
                        "qty": "2.00000000",
                        "commission": "7.99600000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3997.00000000",
                        "qty": "1.00000000",
                        "commission": "3.99700000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3995.00000000",
                        "qty": "1.00000000",
                        "commission": "3.99500000",
                        "commissionAsset": "USDT"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        return self._post('order', True, data=params)

    def order_limit(self, timeInForce=TIME_IN_FORCE_GTC, **params):
        """Send in a new limit order

        Any order with an icebergQty MUST have timeInForce set to GTC.

        :param symbol: required
        :type symbol: str
        :param side: required
        :type side: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param timeInForce: default Good till cancelled
        :type timeInForce: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param icebergQty: Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({
            'type': self.ORDER_TYPE_LIMIT,
            'timeInForce': timeInForce
        })
        return self.create_order(**params)

    def order_limit_buy(self, timeInForce=TIME_IN_FORCE_GTC, **params):
        """Send in a new limit buy order

        Any order with an icebergQty MUST have timeInForce set to GTC.

        :param symbol: required
        :type symbol: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param timeInForce: default Good till cancelled
        :type timeInForce: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param stopPrice: Used with stop orders
        :type stopPrice: decimal
        :param icebergQty: Used with iceberg orders
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({
            'side': self.SIDE_BUY,
        })
        return self.order_limit(timeInForce=timeInForce, **params)

    def order_limit_sell(self, timeInForce=TIME_IN_FORCE_GTC, **params):
        """Send in a new limit sell order

        :param symbol: required
        :type symbol: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param timeInForce: default Good till cancelled
        :type timeInForce: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param stopPrice: Used with stop orders
        :type stopPrice: decimal
        :param icebergQty: Used with iceberg orders
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({
            'side': self.SIDE_SELL
        })
        return self.order_limit(timeInForce=timeInForce, **params)

    def order_market(self, **params):
        """Send in a new market order

        :param symbol: required
        :type symbol: str
        :param side: required
        :type side: str
        :param quantity: required
        :type quantity: decimal
        :param quoteOrderQty: amount the user wants to spend (when buying) or receive (when selling)
            of the quote asset
        :type quoteOrderQty: decimal
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({
            'type': self.ORDER_TYPE_MARKET
        })
        return self.create_order(**params)

    def order_market_buy(self, **params):
        """Send in a new market buy order

        :param symbol: required
        :type symbol: str
        :param quantity: required
        :type quantity: decimal
        :param quoteOrderQty: the amount the user wants to spend of the quote asset
        :type quoteOrderQty: decimal
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({
            'side': self.SIDE_BUY
        })
        return self.order_market(**params)

    def order_market_sell(self, **params):
        """Send in a new market sell order

        :param symbol: required
        :type symbol: str
        :param quantity: required
        :type quantity: decimal
        :param quoteOrderQty: the amount the user wants to receive of the quote asset
        :type quoteOrderQty: decimal
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({
            'side': self.SIDE_SELL
        })
        return self.order_market(**params)

    def create_oco_order(self, **params):
        """Send in a new OCO order

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#new-oco-trade

        :param symbol: required
        :type symbol: str
        :param listClientOrderId: A unique id for the list order. Automatically generated if not sent.
        :type listClientOrderId: str
        :param side: required
        :type side: str
        :param quantity: required
        :type quantity: decimal
        :param limitClientOrderId: A unique id for the limit order. Automatically generated if not sent.
        :type limitClientOrderId: str
        :param price: required
        :type price: str
        :param limitIcebergQty: Used to make the LIMIT_MAKER leg an iceberg order.
        :type limitIcebergQty: decimal
        :param stopClientOrderId: A unique id for the stop order. Automatically generated if not sent.
        :type stopClientOrderId: str
        :param stopPrice: required
        :type stopPrice: str
        :param stopLimitPrice: If provided, stopLimitTimeInForce is required.
        :type stopLimitPrice: str
        :param stopIcebergQty: Used with STOP_LOSS_LIMIT leg to make an iceberg order.
        :type stopIcebergQty: decimal
        :param stopLimitTimeInForce: Valid values are GTC/FOK/IOC.
        :type stopLimitTimeInForce: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        Response ACK:

        .. code-block:: python

            {
            }

        Response RESULT:

        .. code-block:: python

            {
            }

        Response FULL:

        .. code-block:: python

            {
            }

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        return self._post('order/oco', True, data=params)

    def order_oco_buy(self, **params):
        """Send in a new OCO buy order

        :param symbol: required
        :type symbol: str
        :param listClientOrderId: A unique id for the list order. Automatically generated if not sent.
        :type listClientOrderId: str
        :param quantity: required
        :type quantity: decimal
        :param limitClientOrderId: A unique id for the limit order. Automatically generated if not sent.
        :type limitClientOrderId: str
        :param price: required
        :type price: str
        :param limitIcebergQty: Used to make the LIMIT_MAKER leg an iceberg order.
        :type limitIcebergQty: decimal
        :param stopClientOrderId: A unique id for the stop order. Automatically generated if not sent.
        :type stopClientOrderId: str
        :param stopPrice: required
        :type stopPrice: str
        :param stopLimitPrice: If provided, stopLimitTimeInForce is required.
        :type stopLimitPrice: str
        :param stopIcebergQty: Used with STOP_LOSS_LIMIT leg to make an iceberg order.
        :type stopIcebergQty: decimal
        :param stopLimitTimeInForce: Valid values are GTC/FOK/IOC.
        :type stopLimitTimeInForce: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See OCO order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({
            'side': self.SIDE_BUY
        })
        return self.create_oco_order(**params)

    def order_oco_sell(self, **params):
        """Send in a new OCO sell order

        :param symbol: required
        :type symbol: str
        :param listClientOrderId: A unique id for the list order. Automatically generated if not sent.
        :type listClientOrderId: str
        :param quantity: required
        :type quantity: decimal
        :param limitClientOrderId: A unique id for the limit order. Automatically generated if not sent.
        :type limitClientOrderId: str
        :param price: required
        :type price: str
        :param limitIcebergQty: Used to make the LIMIT_MAKER leg an iceberg order.
        :type limitIcebergQty: decimal
        :param stopClientOrderId: A unique id for the stop order. Automatically generated if not sent.
        :type stopClientOrderId: str
        :param stopPrice: required
        :type stopPrice: str
        :param stopLimitPrice: If provided, stopLimitTimeInForce is required.
        :type stopLimitPrice: str
        :param stopIcebergQty: Used with STOP_LOSS_LIMIT leg to make an iceberg order.
        :type stopIcebergQty: decimal
        :param stopLimitTimeInForce: Valid values are GTC/FOK/IOC.
        :type stopLimitTimeInForce: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See OCO order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({
            'side': self.SIDE_SELL
        })
        return self.create_oco_order(**params)

    def create_test_order(self, **params):
        """Test new order creation and signature/recvWindow long. Creates and validates a new order but does not send it into the matching engine.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#test-new-order-trade

        :param symbol: required
        :type symbol: str
        :param side: required
        :type side: str
        :param type: required
        :type type: str
        :param timeInForce: required if limit order
        :type timeInForce: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param icebergQty: Used with iceberg orders
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: The number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException


        """
        return self._post('order/test', True, data=params)

    def get_order(self, **params):
        """Check an order's status. Either orderId or origClientOrderId must be sent.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#query-order-user_data

        :param symbol: required
        :type symbol: str
        :param orderId: The unique order id
        :type orderId: int
        :param origClientOrderId: optional
        :type origClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "symbol": "LTCBTC",
                "orderId": 1,
                "clientOrderId": "myOrder1",
                "price": "0.1",
                "origQty": "1.0",
                "executedQty": "0.0",
                "status": "NEW",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "BUY",
                "stopPrice": "0.0",
                "icebergQty": "0.0",
                "time": 1499827319559
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('order', True, data=params)

    def get_all_orders(self, **params):
        """Get all account orders; active, canceled, or filled.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#all-orders-user_data

        :param symbol: required
        :type symbol: str
        :param orderId: The unique order id
        :type orderId: int
        :param limit: Default 500; max 500.
        :type limit: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "orderId": 1,
                    "clientOrderId": "myOrder1",
                    "price": "0.1",
                    "origQty": "1.0",
                    "executedQty": "0.0",
                    "status": "NEW",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "side": "BUY",
                    "stopPrice": "0.0",
                    "icebergQty": "0.0",
                    "time": 1499827319559
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('allOrders', True, data=params)

    def cancel_order(self, **params):
        """Cancel an active order. Either orderId or origClientOrderId must be sent.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#cancel-order-trade

        :param symbol: required
        :type symbol: str
        :param orderId: The unique order id
        :type orderId: int
        :param origClientOrderId: optional
        :type origClientOrderId: str
        :param newClientOrderId: Used to uniquely identify this cancel. Automatically generated by default.
        :type newClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "symbol": "LTCBTC",
                "origClientOrderId": "myOrder1",
                "orderId": 1,
                "clientOrderId": "cancelMyOrder1"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._delete('order', True, data=params)

    def get_open_orders(self, **params):
        """Get all open orders on a symbol.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#current-open-orders-user_data

        :param symbol: optional
        :type symbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "orderId": 1,
                    "clientOrderId": "myOrder1",
                    "price": "0.1",
                    "origQty": "1.0",
                    "executedQty": "0.0",
                    "status": "NEW",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "side": "BUY",
                    "stopPrice": "0.0",
                    "icebergQty": "0.0",
                    "time": 1499827319559
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('openOrders', True, data=params)

    # User Stream Endpoints
    def get_account(self, **params):
        """Get current account information.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#account-information-user_data

        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "makerCommission": 15,
                "takerCommission": 15,
                "buyerCommission": 0,
                "sellerCommission": 0,
                "canTrade": true,
                "canWithdraw": true,
                "canDeposit": true,
                "balances": [
                    {
                        "asset": "BTC",
                        "free": "4723846.89208129",
                        "locked": "0.00000000"
                    },
                    {
                        "asset": "LTC",
                        "free": "4763368.68006011",
                        "locked": "0.00000000"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('account', True, data=params)

    def get_asset_balance(self, asset, **params):
        """Get current asset balance.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#account-information-user_data

        :param asset: required
        :type asset: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: dictionary or None if not found

        .. code-block:: python

            {
                "asset": "BTC",
                "free": "4723846.89208129",
                "locked": "0.00000000"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        res = self.get_account(**params)
        # find asset balance in list of balances
        if "balances" in res:
            for bal in res['balances']:
                if bal['asset'].lower() == asset.lower():
                    return bal
        return None

    def get_my_trades(self, **params):
        """Get trades for a specific symbol.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#account-trade-list-user_data

        :param symbol: required
        :type symbol: str
        :param limit: Default 500; max 500.
        :type limit: int
        :param fromId: TradeId to fetch from. Default gets most recent trades.
        :type fromId: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "id": 28457,
                    "price": "4.00000100",
                    "qty": "12.00000000",
                    "commission": "10.10000000",
                    "commissionAsset": "BNB",
                    "time": 1499865549590,
                    "isBuyer": true,
                    "isMaker": false,
                    "isBestMatch": true
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('myTrades', True, data=params)

    def get_system_status(self):
        """Get system status detail.

        https://binance-docs.github.io/apidocs/spot/en/#system-status-system

        :returns: API response

        .. code-block:: python

            {
                "status": 0,        # 0: normal，1：system maintenance
                "msg": "normal"     # normal or System maintenance.
            }

        :raises: BinanceAPIException

        """
        return self._request_withdraw_api('get', 'systemStatus.html')

    def get_account_status(self, **params):
        """Get account status detail.

        https://binance-docs.github.io/apidocs/spot/en/#account-status-user_data

        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "msg": "Order failed:Low Order fill rate! Will be reactivated after 5 minutes.",
                "success": true,
                "objs": [
                    "5"
                ]
            }

        :raises: BinanceWithdrawException

        """
        res = self._request_withdraw_api('get', 'accountStatus.html', True, data=params)
        if not res.get('success'):
            raise BinanceWithdrawException(res['msg'])
        return res

    def get_account_api_trading_status(self, **params):
        """Fetch account api trading status detail.

        https://binance-docs.github.io/apidocs/spot/en/#account-api-trading-status-user_data

        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

        {
            "success": true,     // Query result
            "status": {          // API trading status detail
                "isLocked": false,   // API trading function is locked or not
                "plannedRecoverTime": 0,  // If API trading function is locked, this is the planned recover time
                "triggerCondition": {
                        "gcr": 150,  // Number of GTC orders
                        "ifer": 150, // Number of FOK/IOC orders
                        "ufr": 300   // Number of orders
                },
                "indicators": {  // The indicators updated every 30 seconds
                     "BTCUSDT": [  // The symbol
                        {
                            "i": "UFR",  // Unfilled Ratio (UFR)
                            "c": 20,     // Count of all orders
                            "v": 0.05,   // Current UFR value
                            "t": 0.995   // Trigger UFR value
                        },
                        {
                            "i": "IFER", // IOC/FOK Expiration Ratio (IFER)
                            "c": 20,     // Count of FOK/IOC orders
                            "v": 0.99,   // Current IFER value
                            "t": 0.99    // Trigger IFER value
                        },
                        {
                            "i": "GCR",  // GTC Cancellation Ratio (GCR)
                            "c": 20,     // Count of GTC orders
                            "v": 0.99,   // Current GCR value
                            "t": 0.99    // Trigger GCR value
                        }
                    ],
                    "ETHUSDT": [
                        {
                            "i": "UFR",
                            "c": 20,
                            "v": 0.05,
                            "t": 0.995
                        },
                        {
                            "i": "IFER",
                            "c": 20,
                            "v": 0.99,
                            "t": 0.99
                        },
                        {
                            "i": "GCR",
                            "c": 20,
                            "v": 0.99,
                            "t": 0.99
                        }
                    ]
                },
                "updateTime": 1547630471725   // The query result return time
            }
        }


        :raises: BinanceWithdrawException

        """
        res = self._request_withdraw_api('get', 'apiTradingStatus.html', True, data=params)
        if not res.get('success'):
            raise BinanceWithdrawException(res['msg'])
        return res

    def get_dust_log(self, **params):
        """Get log of small amounts exchanged for BNB.

        https://binance-docs.github.io/apidocs/spot/en/#dustlog-user_data

        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "success": true,
                "results": {
                    "total": 2,   //Total counts of exchange
                    "rows": [
                        {
                            "transfered_total": "0.00132256", # Total transfered BNB amount for this exchange.
                            "service_charge_total": "0.00002699",   # Total service charge amount for this exchange.
                            "tran_id": 4359321,
                            "logs": [           # Details of  this exchange.
                                {
                                    "tranId": 4359321,
                                    "serviceChargeAmount": "0.000009",
                                    "uid": "10000015",
                                    "amount": "0.0009",
                                    "operateTime": "2018-05-03 17:07:04",
                                    "transferedAmount": "0.000441",
                                    "fromAsset": "USDT"
                                },
                                {
                                    "tranId": 4359321,
                                    "serviceChargeAmount": "0.00001799",
                                    "uid": "10000015",
                                    "amount": "0.0009",
                                    "operateTime": "2018-05-03 17:07:04",
                                    "transferedAmount": "0.00088156",
                                    "fromAsset": "ETH"
                                }
                            ],
                            "operate_time": "2018-05-03 17:07:04" //The time of this exchange.
                        },
                        {
                            "transfered_total": "0.00058795",
                            "service_charge_total": "0.000012",
                            "tran_id": 4357015,
                            "logs": [       // Details of  this exchange.
                                {
                                    "tranId": 4357015,
                                    "serviceChargeAmount": "0.00001",
                                    "uid": "10000015",
                                    "amount": "0.001",
                                    "operateTime": "2018-05-02 13:52:24",
                                    "transferedAmount": "0.00049",
                                    "fromAsset": "USDT"
                                },
                                {
                                    "tranId": 4357015,
                                    "serviceChargeAmount": "0.000002",
                                    "uid": "10000015",
                                    "amount": "0.0001",
                                    "operateTime": "2018-05-02 13:51:11",
                                    "transferedAmount": "0.00009795",
                                    "fromAsset": "ETH"
                                }
                            ],
                            "operate_time": "2018-05-02 13:51:11"
                        }
                    ]
                }
            }

        :raises: BinanceWithdrawException

        """
        res = self._request_withdraw_api('get', 'userAssetDribbletLog.html', True, data=params)
        if not res.get('success'):
            raise BinanceWithdrawException(res['msg'])
        return res

    def transfer_dust(self, **params):
        """Convert dust assets to BNB.

        https://binance-docs.github.io/apidocs/spot/en/#dust-transfer-user_data

        :param asset: The asset being converted. e.g: 'ONE'
        :type asset: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code:: python

            result = client.transfer_dust(asset='ONE')

        :returns: API response

        .. code-block:: python

            {
                "totalServiceCharge":"0.02102542",
                "totalTransfered":"1.05127099",
                "transferResult":[
                    {
                        "amount":"0.03000000",
                        "fromAsset":"ETH",
                        "operateTime":1563368549307,
                        "serviceChargeAmount":"0.00500000",
                        "tranId":2970932918,
                        "transferedAmount":"0.25000000"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'asset/dust', True, data=params)

    def get_asset_dividend_history(self, **params):
        """Query asset dividend record.

        https://binance-docs.github.io/apidocs/spot/en/#asset-dividend-record-user_data

        :param asset: optional
        :type asset: str
        :param startTime: optional
        :type startTime: long
        :param endTime: optional
        :type endTime: long
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code:: python

            result = client.get_asset_dividend_history()

        :returns: API response

        .. code-block:: python

            {
                "rows":[
                    {
                        "amount":"10.00000000",
                        "asset":"BHFT",
                        "divTime":1563189166000,
                        "enInfo":"BHFT distribution",
                        "tranId":2968885920
                    },
                    {
                        "amount":"10.00000000",
                        "asset":"BHFT",
                        "divTime":1563189165000,
                        "enInfo":"BHFT distribution",
                        "tranId":2968885920
                    }
                ],
                "total":2
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'asset/assetDividend', True, data=params)

    def make_universal_transfer(self, **params):
        """User Universal Transfer

        https://binance-docs.github.io/apidocs/spot/en/#user-universal-transfer

        :param type: required
        :type type: str (ENUM)
        :param asset: required
        :type asset: str
        :param amount: required
        :type amount: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code:: python

            transfer_status = client.make_universal_transfer(params)

        :returns: API response

        .. code-block:: python

            {
                "tranId":13526853623
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'asset/transfer', signed=True, data=params)

    def query_universal_transfer_history(self, **params):
        """Query User Universal Transfer History

        https://binance-docs.github.io/apidocs/spot/en/#query-user-universal-transfer-history

        :param type: required
        :type type: str (ENUM)
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param current: optional - Default 1
        :type current: int
        :param size: required - Default 10, Max 100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code:: python

            transfer_status = client.query_universal_transfer_history(params)

        :returns: API response

        .. code-block:: python

            {
                "total":2,
                "rows":[
                    {
                        "asset":"USDT",
                        "amount":"1",
                        "type":"MAIN_UMFUTURE"
                        "status": "CONFIRMED",
                        "tranId": 11415955596,
                        "timestamp":1544433328000
                    },
                    {
                        "asset":"USDT",
                        "amount":"2",
                        "type":"MAIN_UMFUTURE",
                        "status": "CONFIRMED",
                        "tranId": 11366865406,
                        "timestamp":1544433328000
                    }
                ]
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'asset/transfer', signed=True, data=params)

    def get_trade_fee(self, **params):
        """Get trade fee.

        https://binance-docs.github.io/apidocs/spot/en/#trade-fee-user_data

        :param symbol: optional
        :type symbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "tradeFee": [
                    {
                        "symbol": "ADABNB",
                        "maker": 0.9000,
                        "taker": 1.0000
                    }, {
                        "symbol": "BNBBTC",
                        "maker": 0.3000,
                        "taker": 0.3000
                    }
                ],
                "success": true
            }

        :raises: BinanceWithdrawException

        """
        res = self._request_withdraw_api('get', 'tradeFee.html', True, data=params)
        if not res.get('success'):
            raise BinanceWithdrawException(res['msg'])
        return res

    def get_asset_details(self, **params):
        """Fetch details on assets.

        https://binance-docs.github.io/apidocs/spot/en/#asset-detail-user_data

        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "success": true,
                "assetDetail": {
                    "CTR": {
                        "minWithdrawAmount": "70.00000000", //min withdraw amount
                        "depositStatus": false,//deposit status
                        "withdrawFee": 35, // withdraw fee
                        "withdrawStatus": true, //withdraw status
                        "depositTip": "Delisted, Deposit Suspended" //reason
                    },
                    "SKY": {
                        "minWithdrawAmount": "0.02000000",
                        "depositStatus": true,
                        "withdrawFee": 0.01,
                        "withdrawStatus": true
                    }
                }
            }

        :raises: BinanceWithdrawException

        """
        res = self._request_withdraw_api('get', 'assetDetail.html', True, data=params)
        if not res.get('success'):
            raise BinanceWithdrawException(res['msg'])
        return res

    # Withdraw Endpoints

    def withdraw(self, **params):
        """Submit a withdraw request.

        https://www.binance.com/restapipub.html

        Assumptions:

        - You must have Withdraw permissions enabled on your API key
        - You must have withdrawn to the address specified through the website and approved the transaction via email

        :param asset: required
        :type asset: str
        :type address: required
        :type address: str
        :type addressTag: optional - Secondary address identifier for coins like XRP,XMR etc.
        :param amount: required
        :type amount: decimal
        :param name: optional - Description of the address, default asset value passed will be used
        :type name: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "msg": "success",
                "success": true,
                "id":"7213fea8e94b4a5593d507237e5a555b"
            }

        :raises: BinanceRequestException, BinanceAPIException, BinanceWithdrawException

        """
        # force a name for the withdrawal if one not set
        if 'asset' in params and 'name' not in params:
            params['name'] = params['asset']
        res = self._request_withdraw_api('post', 'withdraw.html', True, data=params)
        if not res.get('success'):
            raise BinanceWithdrawException(res['msg'])
        return res

    def get_deposit_history(self, **params):
        """Fetch deposit history.

        https://www.binance.com/restapipub.html

        :param asset: optional
        :type asset: str
        :type status: 0(0:pending,1:success) optional
        :type status: int
        :param startTime: optional
        :type startTime: long
        :param endTime: optional
        :type endTime: long
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "depositList": [
                    {
                        "insertTime": 1508198532000,
                        "amount": 0.04670582,
                        "asset": "ETH",
                        "status": 1
                    }
                ],
                "success": true
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_withdraw_api('get', 'depositHistory.html', True, data=params)

    def get_withdraw_history(self, **params):
        """Fetch withdraw history.

        https://www.binance.com/restapipub.html

        :param asset: optional
        :type asset: str
        :type status: 0(0:Email Sent,1:Cancelled 2:Awaiting Approval 3:Rejected 4:Processing 5:Failure 6Completed) optional
        :type status: int
        :param startTime: optional
        :type startTime: long
        :param endTime: optional
        :type endTime: long
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "withdrawList": [
                    {
                        "amount": 1,
                        "address": "0x6915f16f8791d0a1cc2bf47c13a6b2a92000504b",
                        "asset": "ETH",
                        "applyTime": 1508198532000
                        "status": 4
                    },
                    {
                        "amount": 0.005,
                        "address": "0x6915f16f8791d0a1cc2bf47c13a6b2a92000504b",
                        "txId": "0x80aaabed54bdab3f6de5868f89929a2371ad21d666f20f7393d1a3389fad95a1",
                        "asset": "ETH",
                        "applyTime": 1508198532000,
                        "status": 4
                    }
                ],
                "success": true
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_withdraw_api('get', 'withdrawHistory.html', True, data=params)

    def get_withdraw_history_id(self, withdraw_id, **params):
        """Fetch withdraw history.

        https://www.binance.com/restapipub.html
        :param withdraw_id: required
        :type withdraw_id: str
        :param asset: optional
        :type asset: str
        :type status: 0(0:Email Sent,1:Cancelled 2:Awaiting Approval 3:Rejected 4:Processing 5:Failure 6Completed) optional
        :type status: int
        :param startTime: optional
        :type startTime: long
        :param endTime: optional
        :type endTime: long
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "amount": 1,
                "address": "0x6915f16f8791d0a1cc2bf47c13a6b2a92000504b",
                "asset": "ETH",
                "applyTime": 1508198532000
                "status": 4
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        result = self._request_withdraw_api('get', 'withdrawHistory.html', True, data=params)

        for entry in result['withdrawList']:
            if 'id' in entry and entry['id'] == withdraw_id:
                return entry
        
        raise Exception("There is no entry with withdraw id", result)

    def get_deposit_address(self, **params):
        """Fetch a deposit address for a symbol

        https://www.binance.com/restapipub.html

        :param asset: required
        :type asset: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "address": "0x6915f16f8791d0a1cc2bf47c13a6b2a92000504b",
                "success": true,
                "addressTag": "1231212",
                "asset": "BNB"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_withdraw_api('get', 'depositAddress.html', True, data=params)

    # User Stream Endpoints

    def stream_get_listen_key(self):
        """Start a new user data stream and return the listen key
        If a stream already exists it should return the same key.
        If the stream becomes invalid a new key is returned.

        Can be used to keep the user stream alive.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#start-user-data-stream-user_stream

        :returns: API response

        .. code-block:: python

            {
                "listenKey": "pqia91ma19a5s61cv6a81va65sdf19v8a65a1a5s61cv6a81va65sdf19v8a65a1"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        res = self._post('userDataStream', False, data={}, version=self.PRIVATE_API_VERSION)
        return res['listenKey']

    def stream_keepalive(self, listenKey):
        """PING a user data stream to prevent a time out.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#keepalive-user-data-stream-user_stream

        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {
            'listenKey': listenKey
        }
        return self._put('userDataStream', False, data=params, version=self.PRIVATE_API_VERSION)

    def stream_close(self, listenKey):
        """Close out a user data stream.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#close-user-data-stream-user_stream

        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {
            'listenKey': listenKey
        }
        return self._delete('userDataStream', False, data=params, version=self.PRIVATE_API_VERSION)

    # Margin Trading Endpoints

    def get_margin_account(self, **params):
        """Query cross-margin account details

        https://binance-docs.github.io/apidocs/spot/en/#query-cross-margin-account-details-user_data

        :returns: API response

        .. code-block:: python

            {
                "borrowEnabled": true,
                "marginLevel": "11.64405625",
                "totalAssetOfBtc": "6.82728457",
                "totalLiabilityOfBtc": "0.58633215",
                "totalNetAssetOfBtc": "6.24095242",
                "tradeEnabled": true,
                "transferEnabled": true,
                "userAssets": [
                    {
                        "asset": "BTC",
                        "borrowed": "0.00000000",
                        "free": "0.00499500",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00499500"
                    },
                    {
                        "asset": "BNB",
                        "borrowed": "201.66666672",
                        "free": "2346.50000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "2144.83333328"
                    },
                    {
                        "asset": "ETH",
                        "borrowed": "0.00000000",
                        "free": "0.00000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00000000"
                    },
                    {
                        "asset": "USDT",
                        "borrowed": "0.00000000",
                        "free": "0.00000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00000000"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/account', True, data=params)

    def get_isolated_margin_account(self, **params):
        """Query isolated margin account details

        https://binance-docs.github.io/apidocs/spot/en/#query-isolated-margin-account-info-user_data

        :param symbols: optional up to 5 margin pairs as a comma separated string
        :type asset: str

        .. code:: python

            account_info = client.get_isolated_margin_account()
            account_info = client.get_isolated_margin_account(symbols="BTCUSDT,ETHUSDT")

        :returns: API response

        .. code-block:: python

            If "symbols" is not sent:

                {
                "assets":[
                    {
                        "baseAsset": 
                        {
                        "asset": "BTC",
                        "borrowEnabled": true,
                        "borrowed": "0.00000000",
                        "free": "0.00000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00000000",
                        "netAssetOfBtc": "0.00000000",
                        "repayEnabled": true,
                        "totalAsset": "0.00000000"
                        },
                        "quoteAsset": 
                        {
                        "asset": "USDT",
                        "borrowEnabled": true,
                        "borrowed": "0.00000000",
                        "free": "0.00000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00000000",
                        "netAssetOfBtc": "0.00000000",
                        "repayEnabled": true,
                        "totalAsset": "0.00000000"
                        },
                        "symbol": "BTCUSDT"
                        "isolatedCreated": true, 
                        "marginLevel": "0.00000000", 
                        "marginLevelStatus": "EXCESSIVE", // "EXCESSIVE", "NORMAL", "MARGIN_CALL", "PRE_LIQUIDATION", "FORCE_LIQUIDATION"
                        "marginRatio": "0.00000000",
                        "indexPrice": "10000.00000000"
                        "liquidatePrice": "1000.00000000",
                        "liquidateRate": "1.00000000"
                        "tradeEnabled": true
                    }
                    ],
                    "totalAssetOfBtc": "0.00000000",
                    "totalLiabilityOfBtc": "0.00000000",
                    "totalNetAssetOfBtc": "0.00000000" 
                }

            If "symbols" is sent:

                {
                "assets":[
                    {
                        "baseAsset": 
                        {
                        "asset": "BTC",
                        "borrowEnabled": true,
                        "borrowed": "0.00000000",
                        "free": "0.00000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00000000",
                        "netAssetOfBtc": "0.00000000",
                        "repayEnabled": true,
                        "totalAsset": "0.00000000"
                        },
                        "quoteAsset": 
                        {
                        "asset": "USDT",
                        "borrowEnabled": true,
                        "borrowed": "0.00000000",
                        "free": "0.00000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00000000",
                        "netAssetOfBtc": "0.00000000",
                        "repayEnabled": true,
                        "totalAsset": "0.00000000"
                        },
                        "symbol": "BTCUSDT"
                        "isolatedCreated": true, 
                        "marginLevel": "0.00000000", 
                        "marginLevelStatus": "EXCESSIVE", // "EXCESSIVE", "NORMAL", "MARGIN_CALL", "PRE_LIQUIDATION", "FORCE_LIQUIDATION"
                        "marginRatio": "0.00000000",
                        "indexPrice": "10000.00000000"
                        "liquidatePrice": "1000.00000000",
                        "liquidateRate": "1.00000000"
                        "tradeEnabled": true
                    }
                    ]
                }

        """
        return self._request_margin_api('get', 'margin/isolated/account', True, data=params)

    def get_margin_asset(self, **params):
        """Query cross-margin asset

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-asset-market_data

        :param asset: name of the asset
        :type asset: str

        .. code:: python

            asset_details = client.get_margin_asset(asset='BNB')

        :returns: API response

        .. code-block:: python

            {
                "assetFullName": "Binance Coin",
                "assetName": "BNB",
                "isBorrowable": false,
                "isMortgageable": true,
                "userMinBorrow": "0.00000000",
                "userMinRepay": "0.00000000"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/asset', data=params)

    def get_margin_symbol(self, **params):
        """Query cross-margin symbol info

        https://binance-docs.github.io/apidocs/spot/en/#query-cross-margin-pair-market_data

        :param symbol: name of the symbol pair
        :type symbol: str

        .. code:: python

            pair_details = client.get_margin_symbol(symbol='BTCUSDT')

        :returns: API response

        .. code-block:: python

            {
                "id":323355778339572400,
                "symbol":"BTCUSDT",
                "base":"BTC",
                "quote":"USDT",
                "isMarginTrade":true,
                "isBuyAllowed":true,
                "isSellAllowed":true
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/pair', data=params)

    def create_isolated_margin_account(self, **params):
        """Create isolated margin account for symbol

        https://binance-docs.github.io/apidocs/spot/en/#create-isolated-margin-account-margin

        :param base: Base asset of symbol
        :type base: str
        :param quote: Quote asset of symbol
        :type quote: str

        .. code:: python

            pair_details = client.create_isolated_margin_account(base='USDT', quote='BTC')

        :returns: API response

        .. code-block:: python

            {
                "success": true,
                "symbol": "BTCUSDT"
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'margin/isolated/create', signed=True, data=params)


    def get_isolated_margin_symbol(self, **params):
        """Query isolated margin symbol info

        https://binance-docs.github.io/apidocs/spot/en/#query-isolated-margin-symbol-user_data

        :param symbol: name of the symbol pair
        :type symbol: str

        .. code:: python

            pair_details = client.get_isolated_margin_symbol(symbol='BTCUSDT')

        :returns: API response

        .. code-block:: python

            {
            "symbol":"BTCUSDT",
            "base":"BTC",
            "quote":"USDT",
            "isMarginTrade":true,
            "isBuyAllowed":true,
            "isSellAllowed":true      
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/isolated/pair', signed=True, data=params)

    def get_all_isolated_margin_symbols(self, **params):
        """Query isolated margin symbol info for all pairs

        https://binance-docs.github.io/apidocs/spot/en/#get-all-isolated-margin-symbol-user_data

        .. code:: python

            pair_details = client.get_all_isolated_margin_symbols()

        :returns: API response

        .. code-block:: python

            [
                {
                    "base": "BNB",
                    "isBuyAllowed": true,
                    "isMarginTrade": true,
                    "isSellAllowed": true,
                    "quote": "BTC",
                    "symbol": "BNBBTC"     
                },
                {
                    "base": "TRX",
                    "isBuyAllowed": true,
                    "isMarginTrade": true,
                    "isSellAllowed": true,
                    "quote": "BTC",
                    "symbol": "TRXBTC"    
                }
            ]


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/isolated/allPairs', signed=True, data=params)

    def toggle_bnb_burn_spot_margin(self, **params):
        """Toggle BNB Burn On Spot Trade And Margin Interest

        https://binance-docs.github.io/apidocs/spot/en/#toggle-bnb-burn-on-spot-trade-and-margin-interest-user_data

        :param spotBNBBurn: Determines whether to use BNB to pay for trading fees on SPOT
        :type spotBNBBurn: bool
        :param interestBNBBurn: Determines whether to use BNB to pay for margin loan's interest
        :type interestBNBBurn: bool

        .. code:: python

            response = client.toggle_bnb_burn_spot_margin()

        :returns: API response

        .. code-block:: python

            {
               "spotBNBBurn":true,
               "interestBNBBurn": false
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'bnbBurn', signed=True, data=params)

    def get_bnb_burn_spot_margin(self, **params):
        """Get BNB Burn Status

        https://binance-docs.github.io/apidocs/spot/en/#get-bnb-burn-status-user_data

        .. code:: python

            status = client.get_bnb_burn_spot_margin()

        :returns: API response

        .. code-block:: python

            {
               "spotBNBBurn":true,
               "interestBNBBurn": false
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'bnbBurn', signed=True, data=params)

    def get_margin_price_index(self, **params):
        """Query margin priceIndex

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-priceindex-market_data

        :param symbol: name of the symbol pair
        :type symbol: str

        .. code:: python

            price_index_details = client.get_margin_price_index(symbol='BTCUSDT')

        :returns: API response

        .. code-block:: python

            {
                "calcTime": 1562046418000,
                "price": "0.00333930",
                "symbol": "BNBBTC"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/priceIndex', data=params)

    def transfer_margin_to_spot(self, **params):
        """Execute transfer between cross-margin account and spot account.

        https://binance-docs.github.io/apidocs/spot/en/#cross-margin-account-transfer-margin

        :param asset: name of the asset
        :type asset: str
        :param amount: amount to transfer
        :type amount: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code:: python

            transfer = client.transfer_margin_to_spot(asset='BTC', amount='1.1')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        params['type'] = 2
        return self._request_margin_api('post', 'margin/transfer', signed=True, data=params)

    def transfer_spot_to_margin(self, **params):
        """Execute transfer between spot account and cross-margin account.

        https://binance-docs.github.io/apidocs/spot/en/#cross-margin-account-transfer-margin

        :param asset: name of the asset
        :type asset: str
        :param amount: amount to transfer
        :type amount: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code:: python

            transfer = client.transfer_spot_to_margin(asset='BTC', amount='1.1')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        params['type'] = 1
        return self._request_margin_api('post', 'margin/transfer', signed=True, data=params)


    def transfer_isolated_margin_to_spot(self, **params):
        """Execute transfer between isolated margin account and spot account.

        https://binance-docs.github.io/apidocs/spot/en/#isolated-margin-account-transfer-margin

        :param asset: name of the asset
        :type asset: str
        :param symbol: pair symbol
        :type symbol: str
        :param amount: amount to transfer
        :type amount: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code:: python

            transfer = client.transfer_isolated_margin_to_spot(asset='BTC', 
                                                                symbol='ETHBTC', amount='1.1')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        params['transFrom'] = "ISOLATED_MARGIN"
        params['transTo'] = "SPOT"
        return self._request_margin_api('post', 'margin/isolated/transfer', signed=True, data=params)

    def transfer_spot_to_isolated_margin(self, **params):
        """Execute transfer between spot account and isolated margin account.

        https://binance-docs.github.io/apidocs/spot/en/#isolated-margin-account-transfer-margin

        :param asset: name of the asset
        :type asset: str
        :param symbol: pair symbol
        :type symbol: str
        :param amount: amount to transfer
        :type amount: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code:: python

            transfer = client.transfer_spot_to_isolated_margin(asset='BTC', 
                                                                symbol='ETHBTC', amount='1.1')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        params['transFrom'] = "SPOT"
        params['transTo'] = "ISOLATED_MARGIN"
        return self._request_margin_api('post', 'margin/isolated/transfer', signed=True, data=params)

    def create_margin_loan(self, **params):
        """Apply for a loan in cross-margin or isolated-margin account.

        https://binance-docs.github.io/apidocs/spot/en/#margin-account-borrow-margin

        :param asset: name of the asset
        :type asset: str
        :param amount: amount to transfer
        :type amount: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param symbol: Isolated margin symbol (default blank for cross-margin)
        :type symbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code:: python

            transaction = client.margin_create_loan(asset='BTC', amount='1.1')

            transaction = client.margin_create_loan(asset='BTC', amount='1.1', 
                                                    isIsolated='TRUE', symbol='ETHBTC')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'margin/loan', signed=True, data=params)

    def repay_margin_loan(self, **params):
        """Repay loan in cross-margin or isolated-margin account.

        If amount is more than the amount borrowed, the full loan will be repaid. 

        https://binance-docs.github.io/apidocs/spot/en/#margin-account-repay-margin

        :param asset: name of the asset
        :type asset: str
        :param amount: amount to transfer
        :type amount: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param symbol: Isolated margin symbol (default blank for cross-margin)
        :type symbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code:: python

            transaction = client.margin_repay_loan(asset='BTC', amount='1.1')

            transaction = client.margin_repay_loan(asset='BTC', amount='1.1', 
                                                    isIsolated='TRUE', symbol='ETHBTC')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'margin/repay', signed=True, data=params)

    def create_margin_order(self, **params):
        """Post a new order for margin account.

        https://binance-docs.github.io/apidocs/spot/en/#margin-account-new-order-trade

        :param symbol: required
        :type symbol: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param side: required
        :type side: str
        :param type: required
        :type type: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param stopPrice: Used with STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, and TAKE_PROFIT_LIMIT orders.
        :type stopPrice: str
        :param timeInForce: required if limit order GTC,IOC,FOK
        :type timeInForce: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param icebergQty: Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        :type icebergQty: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; MARKET and LIMIT order types default to
            FULL, all other orders default to ACK.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        Response ACK:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595
            }

        Response RESULT:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595,
                "price": "1.00000000",
                "origQty": "10.00000000",
                "executedQty": "10.00000000",
                "cummulativeQuoteQty": "10.00000000",
                "status": "FILLED",
                "timeInForce": "GTC",
                "type": "MARKET",
                "side": "SELL"
            }

        Response FULL:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595,
                "price": "1.00000000",
                "origQty": "10.00000000",
                "executedQty": "10.00000000",
                "cummulativeQuoteQty": "10.00000000",
                "status": "FILLED",
                "timeInForce": "GTC",
                "type": "MARKET",
                "side": "SELL",
                "fills": [
                    {
                        "price": "4000.00000000",
                        "qty": "1.00000000",
                        "commission": "4.00000000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3999.00000000",
                        "qty": "5.00000000",
                        "commission": "19.99500000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3998.00000000",
                        "qty": "2.00000000",
                        "commission": "7.99600000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3997.00000000",
                        "qty": "1.00000000",
                        "commission": "3.99700000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3995.00000000",
                        "qty": "1.00000000",
                        "commission": "3.99500000",
                        "commissionAsset": "USDT"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException,
            BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
            BinanceOrderInactiveSymbolException

        """
        return self._request_margin_api('post', 'margin/order', signed=True, data=params)

    def cancel_margin_order(self, **params):
        """Cancel an active order for margin account.

        Either orderId or origClientOrderId must be sent.

        https://binance-docs.github.io/apidocs/spot/en/#margin-account-cancel-order-trade

        :param symbol: required
        :type symbol: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param orderId:
        :type orderId: str
        :param origClientOrderId:
        :type origClientOrderId: str
        :param newClientOrderId: Used to uniquely identify this cancel. Automatically generated by default.
        :type newClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "symbol": "LTCBTC",
                "orderId": 28,
                "origClientOrderId": "myOrder1",
                "clientOrderId": "cancelMyOrder1",
                "transactTime": 1507725176595,
                "price": "1.00000000",
                "origQty": "10.00000000",
                "executedQty": "8.00000000",
                "cummulativeQuoteQty": "8.00000000",
                "status": "CANCELED",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "SELL"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('delete', 'margin/order', signed=True, data=params)

    def get_margin_loan_details(self, **params):
        """Query loan record

        txId or startTime must be sent. txId takes precedence.

        https://binance-docs.github.io/apidocs/spot/en/#query-loan-record-user_data

        :param asset: required
        :type asset: str
        :param isolatedSymbol: isolated symbol (if querying isolated margin)
        :type isolatedSymbol: str
        :param txId: the tranId in of the created loan
        :type txId: str
        :param startTime: earliest timestamp to filter transactions
        :type startTime: str
        :param endTime: Used to uniquely identify this cancel. Automatically generated by default.
        :type endTime: str
        :param current: Currently querying page. Start from 1. Default:1
        :type current: str
        :param size: Default:10 Max:100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "rows": [
                    {
                        "asset": "BNB",
                        "principal": "0.84624403",
                        "timestamp": 1555056425000,
                        //one of PENDING (pending to execution), CONFIRMED (successfully loaned), FAILED (execution failed, nothing happened to your account);
                        "status": "CONFIRMED"
                    }
                ],
                "total": 1
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/loan', signed=True, data=params)

    def get_margin_repay_details(self, **params):
        """Query repay record

        txId or startTime must be sent. txId takes precedence.

        https://binance-docs.github.io/apidocs/spot/en/#query-repay-record-user_data

        :param asset: required
        :type asset: str
        :param isolatedSymbol: isolated symbol (if querying isolated margin)
        :type isolatedSymbol: str
        :param txId: the tranId in of the created loan
        :type txId: str
        :param startTime:
        :type startTime: str
        :param endTime: Used to uniquely identify this cancel. Automatically generated by default.
        :type endTime: str
        :param current: Currently querying page. Start from 1. Default:1
        :type current: str
        :param size: Default:10 Max:100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "rows": [
                    {
                        //Total amount repaid
                        "amount": "14.00000000",
                        "asset": "BNB",
                        //Interest repaid
                        "interest": "0.01866667",
                        //Principal repaid
                        "principal": "13.98133333",
                        //one of PENDING (pending to execution), CONFIRMED (successfully loaned), FAILED (execution failed, nothing happened to your account);
                        "status": "CONFIRMED",
                        "timestamp": 1563438204000,
                        "txId": 2970933056
                    }
                ],
                "total": 1
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/repay', signed=True, data=params)

    def get_margin_order(self, **params):
        """Query margin accounts order

        Either orderId or origClientOrderId must be sent.

        For some historical orders cummulativeQuoteQty will be < 0, meaning the data is not available at this time.

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-order-user_data

        :param symbol: required
        :type symbol: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param orderId:
        :type orderId: str
        :param origClientOrderId:
        :type origClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "clientOrderId": "ZwfQzuDIGpceVhKW5DvCmO",
                "cummulativeQuoteQty": "0.00000000",
                "executedQty": "0.00000000",
                "icebergQty": "0.00000000",
                "isWorking": true,
                "orderId": 213205622,
                "origQty": "0.30000000",
                "price": "0.00493630",
                "side": "SELL",
                "status": "NEW",
                "stopPrice": "0.00000000",
                "symbol": "BNBBTC",
                "time": 1562133008725,
                "timeInForce": "GTC",
                "type": "LIMIT",
                "updateTime": 1562133008725
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/order', signed=True, data=params)

    def get_open_margin_orders(self, **params):
        """Query margin accounts open orders

        If the symbol is not sent, orders for all symbols will be returned in an array (cross-margin only).

        If querying isolated margin orders, both the isIsolated='TRUE' and symbol=symbol_name must be set.

        When all symbols are returned, the number of requests counted against the rate limiter is equal to the number
        of symbols currently trading on the exchange.

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-open-order-user_data

        :param symbol: optional
        :type symbol: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            [
                {
                    "clientOrderId": "qhcZw71gAkCCTv0t0k8LUK",
                    "cummulativeQuoteQty": "0.00000000",
                    "executedQty": "0.00000000",
                    "icebergQty": "0.00000000",
                    "isWorking": true,
                    "orderId": 211842552,
                    "origQty": "0.30000000",
                    "price": "0.00475010",
                    "side": "SELL",
                    "status": "NEW",
                    "stopPrice": "0.00000000",
                    "symbol": "BNBBTC",
                    "time": 1562040170089,
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "updateTime": 1562040170089
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/openOrders', signed=True, data=params)

    def get_all_margin_orders(self, **params):
        """Query all margin accounts orders

        If orderId is set, it will get orders >= that orderId. Otherwise most recent orders are returned.

        For some historical orders cummulativeQuoteQty will be < 0, meaning the data is not available at this time.

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-all-order-user_data

        :param symbol: required
        :type symbol: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param orderId: optional
        :type orderId: str
        :param startTime: optional
        :type startTime: str
        :param endTime: optional
        :type endTime: str
        :param limit: Default 500; max 1000
        :type limit: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            [
                {
                    "id": 43123876,
                    "price": "0.00395740",
                    "qty": "4.06000000",
                    "quoteQty": "0.01606704",
                    "symbol": "BNBBTC",
                    "time": 1556089977693
                },
                {
                    "id": 43123877,
                    "price": "0.00395740",
                    "qty": "0.77000000",
                    "quoteQty": "0.00304719",
                    "symbol": "BNBBTC",
                    "time": 1556089977693
                },
                {
                    "id": 43253549,
                    "price": "0.00428930",
                    "qty": "23.30000000",
                    "quoteQty": "0.09994069",
                    "symbol": "BNBBTC",
                    "time": 1556163963504
                }
            ]


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/allOrders', signed=True, data=params)

    def get_margin_trades(self, **params):
        """Query margin accounts trades

        If fromId is set, it will get orders >= that fromId. Otherwise most recent orders are returned.

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-trade-list-user_data

        :param symbol: required
        :type symbol: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param fromId: optional
        :type fromId: str
        :param startTime: optional
        :type startTime: str
        :param endTime: optional
        :type endTime: str
        :param limit: Default 500; max 1000
        :type limit: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            [
                {
                    "commission": "0.00006000",
                    "commissionAsset": "BTC",
                    "id": 34,
                    "isBestMatch": true,
                    "isBuyer": false,
                    "isMaker": false,
                    "orderId": 39324,
                    "price": "0.02000000",
                    "qty": "3.00000000",
                    "symbol": "BNBBTC",
                    "time": 1561973357171
                }, {
                    "commission": "0.00002950",
                    "commissionAsset": "BTC",
                    "id": 32,
                    "isBestMatch": true,
                    "isBuyer": false,
                    "isMaker": true,
                    "orderId": 39319,
                    "price": "0.00590000",
                    "qty": "5.00000000",
                    "symbol": "BNBBTC",
                    "time": 1561964645345
                }
            ]


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/myTrades', signed=True, data=params)

    def get_max_margin_loan(self, **params):
        """Query max borrow amount for an asset

        https://binance-docs.github.io/apidocs/spot/en/#query-max-borrow-user_data

        :param asset: required
        :type asset: str
        :param isolatedSymbol: isolated symbol (if querying isolated margin)
        :type isolatedSymbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "amount": "1.69248805"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/maxBorrowable', signed=True, data=params)

    def get_max_margin_transfer(self, **params):
        """Query max transfer-out amount

        https://binance-docs.github.io/apidocs/spot/en/#query-max-transfer-out-amount-user_data

        :param asset: required
        :type asset: str
        :param isolatedSymbol: isolated symbol (if querying isolated margin)
        :type isolatedSymbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "amount": "3.59498107"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/maxTransferable', signed=True, data=params)

    # Cross-margin 

    def margin_stream_get_listen_key(self):
        """Start a new cross-margin data stream and return the listen key
        If a stream already exists it should return the same key.
        If the stream becomes invalid a new key is returned.

        Can be used to keep the stream alive.

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-margin

        :returns: API response

        .. code-block:: python

            {
                "listenKey": "pqia91ma19a5s61cv6a81va65sdf19v8a65a1a5s61cv6a81va65sdf19v8a65a1"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        res = self._request_margin_api('post', 'userDataStream', signed=False, data={})
        return res['listenKey']

    def margin_stream_keepalive(self, listenKey):
        """PING a cross-margin data stream to prevent a time out.

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-margin

        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {
            'listenKey': listenKey
        }
        return self._request_margin_api('put', 'userDataStream', signed=False, data=params)

    def margin_stream_close(self, listenKey):
        """Close out a cross-margin data stream.

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-margin

        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {
            'listenKey': listenKey
        }
        return self._request_margin_api('delete', 'userDataStream', signed=False, data=params)

    # Isolated margin 

    def isolated_margin_stream_get_listen_key(self, symbol):
        """Start a new isolated margin data stream and return the listen key
        If a stream already exists it should return the same key.
        If the stream becomes invalid a new key is returned.

        Can be used to keep the stream alive.

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-isolated-margin

        :param symbol: required - symbol for the isolated margin account
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "listenKey":  "T3ee22BIYuWqmvne0HNq2A2WsFlEtLhvWCtItw6ffhhdmjifQ2tRbuKkTHhr"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {
            'symbol': symbol
        }
        res = self._request_margin_api('post', 'userDataStream/isolated', signed=False, data=params)
        return res['listenKey']

    def isolated_margin_stream_keepalive(self, symbol, listenKey):
        """PING an isolated margin data stream to prevent a time out.

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-isolated-margin

        :param symbol: required - symbol for the isolated margin account
        :type symbol: str
        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {
            'symbol': symbol,
            'listenKey': listenKey
        }
        return self._request_margin_api('put', 'userDataStream/isolated', signed=False, data=params)

    def isolated_margin_stream_close(self, symbol, listenKey):
        """Close out an isolated margin data stream.

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-isolated-margin

        :param symbol: required - symbol for the isolated margin account
        :type symbol: str
        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {
            'symbol': symbol,
            'listenKey': listenKey
        }
        return self._request_margin_api('delete', 'userDataStream/isolated', signed=False, data=params)

    # Lending Endpoints

    def get_lending_product_list(self, **params):
        """Get Lending Product List

        https://binance-docs.github.io/apidocs/spot/en/#get-flexible-product-list-user_data

        """
        return self._request_margin_api('get', 'lending/daily/product/list', signed=True, data=params)

    def get_lending_daily_quota_left(self, **params):
        """Get Left Daily Purchase Quota of Flexible Product.

        https://binance-docs.github.io/apidocs/spot/en/#get-left-daily-purchase-quota-of-flexible-product-user_data

        """
        return self._request_margin_api('get', 'lending/daily/userLeftQuota', signed=True, data=params)

    def purchase_lending_product(self, **params):
        """Purchase Flexible Product

        https://binance-docs.github.io/apidocs/spot/en/#purchase-flexible-product-user_data

        """
        return self._request_margin_api('post', 'lending/daily/purchase', signed=True, data=params)

    def get_lending_daily_redemption_quota(self, **params):
        """Get Left Daily Redemption Quota of Flexible Product

        https://binance-docs.github.io/apidocs/spot/en/#get-left-daily-redemption-quota-of-flexible-product-user_data

        """
        return self._request_margin_api('get', 'lending/daily/userRedemptionQuota', signed=True, data=params)

    def redeem_lending_product(self, **params):
        """Redeem Flexible Product

        https://binance-docs.github.io/apidocs/spot/en/#redeem-flexible-product-user_data

        """
        return self._request_margin_api('post', 'lending/daily/redeem', signed=True, data=params)

    def get_lending_position(self, **params):
        """Get Flexible Product Position

        https://binance-docs.github.io/apidocs/spot/en/#get-flexible-product-position-user_data

        """
        return self._request_margin_api('get', 'lending/daily/token/position', signed=True, data=params)

    def get_fixed_activity_project_list(self, **params):
        """Get Fixed and Activity Project List

        https://binance-docs.github.io/apidocs/spot/en/#get-fixed-and-activity-project-list-user_data

        :param asset: optional
        :type asset: str
		:param type: required - "ACTIVITY", "CUSTOMIZED_FIXED"
		:type type: str
		:param status: optional - "ALL", "SUBSCRIBABLE", "UNSUBSCRIBABLE"; default "ALL"
		:type status: str
		:param sortBy: optional - "START_TIME", "LOT_SIZE", "INTEREST_RATE", "DURATION"; default "START_TIME"
		:type sortBy: str
		:param current: optional - Currently querying page. Start from 1. Default:1
		:type current: int
		:param size: optional - Default:10, Max:100
		:type size: int
	    :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "asset": "USDT",
                    "displayPriority": 1,
                    "duration": 90,
                    "interestPerLot": "1.35810000",
                    "interestRate": "0.05510000",
                    "lotSize": "100.00000000",
                    "lotsLowLimit": 1,
                    "lotsPurchased": 74155,
                    "lotsUpLimit": 80000,
                    "maxLotsPerUser": 2000,
                    "needKyc": False,
                    "projectId": "CUSDT90DAYSS001",
                    "projectName": "USDT",
                    "status": "PURCHASING",
                    "type": "CUSTOMIZED_FIXED",
                    "withAreaLimitation": False
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException
        
        """
        return self._request_margin_api('get', 'lending/project/list', signed=True, data=params)

    def get_lending_account(self, **params):
        """Get Lending Account Details

        https://binance-docs.github.io/apidocs/spot/en/#lending-account-user_data

        """
        return self._request_margin_api('get', 'lending/union/account', signed=True, data=params)

    def get_lending_purchase_history(self, **params):
        """Get Lending Purchase History

        https://binance-docs.github.io/apidocs/spot/en/#get-purchase-record-user_data

        """
        return self._request_margin_api('get', 'lending/union/purchaseRecord', signed=True, data=params)

    def get_lending_redemption_history(self, **params):
        """Get Lending Redemption History

        https://binance-docs.github.io/apidocs/spot/en/#get-redemption-record-user_data

        """
        return self._request_margin_api('get', 'lending/union/redemptionRecord', signed=True, data=params)

    def get_lending_interest_history(self, **params):
        """Get Lending Interest History

        https://binance-docs.github.io/apidocs/spot/en/#get-interest-history-user_data-2

        """
        return self._request_margin_api('get', 'lending/union/interestHistory', signed=True, data=params)

    def change_fixed_activity_to_daily_position(self, **params):
        """Change Fixed/Activity Position to Daily Position

        https://binance-docs.github.io/apidocs/spot/en/#change-fixed-activity-position-to-daily-position-user_data

        """
        return self._request_margin_api('post', 'lending/positionChanged', signed=True, data=params)

    # Sub Accounts

    def get_sub_account_list(self, **params):
        """Query Sub-account List.

        https://binance-docs.github.io/apidocs/spot/en/#query-sub-account-list-for-master-account

        :param email: optional
        :type email: str
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param page: optional
        :type page: int
        :param limit: optional
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "success":true,
                "subAccounts":[
                    {
                        "email":"123@test.com",
                        "status":"enabled",
                        "activated":true,
                        "mobile":"91605290",
                        "gAuth":true,
                        "createTime":1544433328000
                    },
                    {
                        "email":"321@test.com",
                        "status":"disabled",
                        "activated":true,
                        "mobile":"22501238",
                        "gAuth":true,
                        "createTime":1544433328000
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_withdraw_api('get', 'sub-account/list.html', True, data=params)

    def get_sub_account_transfer_history(self, **params):
        """Query Sub-account Transfer History.

        https://binance-docs.github.io/apidocs/spot/en/#query-sub-account-spot-asset-transfer-history-for-master-account

        :param email: required
        :type email: str
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param page: optional
        :type page: int
        :param limit: optional
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "success":true,
                "transfers":[
                    {
                        "from":"aaa@test.com",
                        "to":"bbb@test.com",
                        "asset":"BTC",
                        "qty":"1",
                        "time":1544433328000
                    },
                    {
                        "from":"bbb@test.com",
                        "to":"ccc@test.com",
                        "asset":"ETH",
                        "qty":"2",
                        "time":1544433328000
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_withdraw_api('get', 'sub-account/transfer/history.html', True, data=params)

    def create_sub_account_transfer(self, **params):
        """Execute sub-account transfer

        https://binance-docs.github.io/apidocs/spot/en/#sub-account-spot-asset-transfer-for-master-account

        :param fromEmail: required - Sender email
        :type fromEmail: str
        :param toEmail: required - Recipient email
        :type toEmail: str
        :param asset: required
        :type asset: str
        :param amount: required
        :type amount: decimal
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "success":true,
                "txnId":"2966662589"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_withdraw_api('post', 'sub-account/transfer.html', True, data=params)
    
    def get_sub_account_futures_transfer_history(self, **params):
        """Query Sub-account Futures Transfer History.

        https://binance-docs.github.io/apidocs/spot/en/#query-sub-account-futures-asset-transfer-history-for-master-account

        :param email: required
        :type email: str
        :param futuresType: required
        :type futuresType: int
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param page: optional
        :type page: int
        :param limit: optional
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "success":true,
                "futuresType": 2,
                "transfers":[
                    {
                        "from":"aaa@test.com",
                        "to":"bbb@test.com",
                        "asset":"BTC",
                        "qty":"1",
                        "time":1544433328000
                    },
                    {
                        "from":"bbb@test.com",
                        "to":"ccc@test.com",
                        "asset":"ETH",
                        "qty":"2",
                        "time":1544433328000
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/futures/internalTransfer', True, data=params)

    def create_sub_account_futures_transfer(self, **params):
        """Execute sub-account Futures transfer

        https://github.com/binance-exchange/binance-official-api-docs/blob/9dbe0e961b80557bb19708a707c7fad08842b28e/wapi-api.md#sub-account-transferfor-master-account

        :param fromEmail: required - Sender email
        :type fromEmail: str
        :param toEmail: required - Recipient email
        :type toEmail: str
        :param futuresType: required
        :type futuresType: int
        :param asset: required
        :type asset: str
        :param amount: required
        :type amount: decimal
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           {
                "success":true,
                "txnId":"2934662589"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'sub-account/futures/internalTransfer', True, data=params)

    def get_sub_account_assets(self, **params):
        """Fetch sub-account assets

        https://binance-docs.github.io/apidocs/spot/en/#query-sub-account-assets-for-master-account

        :param email: required
        :type email: str
        :param symbol: optional
        :type symbol: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "success":true,
                "balances":[
                    {
                        "asset":"ADA",
                        "free":10000,
                        "locked":0
                    },
                    {
                        "asset":"BNB",
                        "free":10003,
                        "locked":0
                    },
                    {
                        "asset":"BTC",
                        "free":11467.6399,
                        "locked":0
                    },
                    {
                        "asset":"ETH",
                        "free":10004.995,
                        "locked":0
                    },
                    {
                        "asset":"USDT",
                        "free":11652.14213,
                        "locked":0
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_withdraw_api('get', 'sub-account/assets.html', True, data=params)

    def query_subaccount_spot_summary(self, **params):
        """Query Sub-account Spot Assets Summary (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#query-sub-account-spot-assets-summary-for-master-account

        :param email: optional - Sub account email
        :type email: str
        :param page: optional - default 1
        :type page: int
        :param size: optional - default 10, max 20
        :type size: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           {
                "totalCount":2,
                "masterAccountTotalAsset": "0.23231201",
                "spotSubUserAssetBtcVoList":[
                    {
                        "email":"sub123@test.com",
                        "totalAsset":"9999.00000000"
                    },
                    {
                        "email":"test456@test.com",
                        "totalAsset":"0.00000000"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/spotSummary', True, data=params)

    def get_subaccount_deposit_address(self, **params):
        """Get Sub-account Deposit Address (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#get-sub-account-deposit-address-for-master-account

        :param email: required - Sub account email
        :type email: str
        :param coin: required
        :type coin: str
        :param network: optional
        :type network: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           {
                "address":"TDunhSa7jkTNuKrusUTU1MUHtqXoBPKETV",
                "coin":"USDT",
                "tag":"",
                "url":"https://tronscan.org/#/address/TDunhSa7jkTNuKrusUTU1MUHtqXoBPKETV"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'capital/deposit/subAddress', True, data=params)

    def get_subaccount_deposit_history(self, **params):
        """Get Sub-account Deposit History (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#get-sub-account-deposit-address-for-master-account

        :param email: required - Sub account email
        :type email: str
        :param coin: optional
        :type coin: str
        :param status: optional - (0:pending,6: credited but cannot withdraw, 1:success)
        :type status: int
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param limit: optional
        :type limit: int
        :param offset: optional - default:0
        :type offset: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           [
                {
                    "amount":"0.00999800",
                    "coin":"PAXG",
                    "network":"ETH",
                    "status":1,
                    "address":"0x788cabe9236ce061e5a892e1a59395a81fc8d62c",
                    "addressTag":"",
                    "txId":"0xaad4654a3234aa6118af9b4b335f5ae81c360b2394721c019b5d1e75328b09f3",
                    "insertTime":1599621997000,
                    "transferType":0,
                    "confirmTimes":"12/12"
                },
                {
                    "amount":"0.50000000",
                    "coin":"IOTA",
                    "network":"IOTA",
                    "status":1,
                    "address":"SIZ9VLMHWATXKV99LH99CIGFJFUMLEHGWVZVNNZXRJJVWBPHYWPPBOSDORZ9EQSHCZAMPVAPGFYQAUUV9DROOXJLNW",
                    "addressTag":"",
                    "txId":"ESBFVQUTPIWQNJSPXFNHNYHSQNTGKRVKPRABQWTAXCDWOAKDKYWPTVG9BGXNVNKTLEJGESAVXIKIZ9999",
                    "insertTime":1599620082000,
                    "transferType":0,
                    "confirmTimes":"1/1"
                }
           ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'capital/deposit/subHisrec', True, data=params)

    def get_subaccount_futures_margin_status(self, **params):
        """Get Sub-account's Status on Margin/Futures (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#get-sub-account-39-s-status-on-margin-futures-for-master-account

        :param email: optional - Sub account email
        :type email: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           [
                {
                    "email":"123@test.com",      // user email
                    "isSubUserEnabled": true,    // true or false
                    "isUserActive": true,        // true or false
                    "insertTime": 1570791523523  // sub account create time
                    "isMarginEnabled": true,     // true or false for margin
                    "isFutureEnabled": true      // true or false for futures.
                    "mobile": 1570791523523      // user mobile number
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/status', True, data=params)

    def enable_subaccount_margin(self, **params):
        """Enable Margin for Sub-account (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#enable-margin-for-sub-account-for-master-account

        :param email: required - Sub account email
        :type email: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           {

                "email":"123@test.com",

                "isMarginEnabled": true

            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'sub-account/margin/enable', True, data=params)

    def get_subaccount_margin_details(self, **params):
        """Get Detail on Sub-account's Margin Account (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#get-detail-on-sub-account-39-s-margin-account-for-master-account

        :param email: required - Sub account email
        :type email: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                  "email":"123@test.com",
                  "marginLevel": "11.64405625",
                  "totalAssetOfBtc": "6.82728457",
                  "totalLiabilityOfBtc": "0.58633215",
                  "totalNetAssetOfBtc": "6.24095242",
                  "marginTradeCoeffVo":
                        {
                            "forceLiquidationBar": "1.10000000",  // Liquidation margin ratio
                            "marginCallBar": "1.50000000",        // Margin call margin ratio
                            "normalBar": "2.00000000"             // Initial margin ratio
                        },
                  "marginUserAssetVoList": [
                      {
                          "asset": "BTC",
                          "borrowed": "0.00000000",
                          "free": "0.00499500",
                          "interest": "0.00000000",
                          "locked": "0.00000000",
                          "netAsset": "0.00499500"
                      },
                      {
                          "asset": "BNB",
                          "borrowed": "201.66666672",
                          "free": "2346.50000000",
                          "interest": "0.00000000",
                          "locked": "0.00000000",
                          "netAsset": "2144.83333328"
                      },
                      {
                          "asset": "ETH",
                          "borrowed": "0.00000000",
                          "free": "0.00000000",
                          "interest": "0.00000000",
                          "locked": "0.00000000",
                          "netAsset": "0.00000000"
                      },
                      {
                          "asset": "USDT",
                          "borrowed": "0.00000000",
                          "free": "0.00000000",
                          "interest": "0.00000000",
                          "locked": "0.00000000",
                          "netAsset": "0.00000000"
                      }
                  ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/margin/account', True, data=params)

    def get_subaccount_margin_summary(self, **params):
        """Get Summary of Sub-account's Margin Account (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#get-summary-of-sub-account-39-s-margin-account-for-master-account

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "totalAssetOfBtc": "4.33333333",
                "totalLiabilityOfBtc": "2.11111112",
                "totalNetAssetOfBtc": "2.22222221",
                "subAccountList":[
                    {
                        "email":"123@test.com",
                        "totalAssetOfBtc": "2.11111111",
                        "totalLiabilityOfBtc": "1.11111111",
                        "totalNetAssetOfBtc": "1.00000000"
                    },
                    {
                        "email":"345@test.com",
                        "totalAssetOfBtc": "2.22222222",
                        "totalLiabilityOfBtc": "1.00000001",
                        "totalNetAssetOfBtc": "1.22222221"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/margin/accountSummary', True, data=params)

    def enable_subaccount_futures(self, **params):
        """Enable Futures for Sub-account (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#enable-futures-for-sub-account-for-master-account

        :param email: required - Sub account email
        :type email: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {

                "email":"123@test.com",

                "isFuturesEnabled": true  // true or false

            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'sub-account/futures/enable', True, data=params)

    def get_subaccount_futures_details(self, **params):
        """Get Detail on Sub-account's Futures Account (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#get-detail-on-sub-account-39-s-futures-account-for-master-account

        :param email: required - Sub account email
        :type email: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "email": "abc@test.com",
                "asset": "USDT",
                "assets":[
                    {
                        "asset": "USDT",
                        "initialMargin": "0.00000000",
                        "maintenanceMargin": "0.00000000",
                        "marginBalance": "0.88308000",
                        "maxWithdrawAmount": "0.88308000",
                        "openOrderInitialMargin": "0.00000000",
                        "positionInitialMargin": "0.00000000",
                        "unrealizedProfit": "0.00000000",
                        "walletBalance": "0.88308000"
                     }
                ],
                "canDeposit": true,
                "canTrade": true,
                "canWithdraw": true,
                "feeTier": 2,
                "maxWithdrawAmount": "0.88308000",
                "totalInitialMargin": "0.00000000",
                "totalMaintenanceMargin": "0.00000000",
                "totalMarginBalance": "0.88308000",
                "totalOpenOrderInitialMargin": "0.00000000",
                "totalPositionInitialMargin": "0.00000000",
                "totalUnrealizedProfit": "0.00000000",
                "totalWalletBalance": "0.88308000",
                "updateTime": 1576756674610
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/futures/account', True, data=params)

    def get_subaccount_futures_summary(self, **params):
        """Get Summary of Sub-account's Futures Account (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#get-summary-of-sub-account-39-s-futures-account-for-master-account

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "totalInitialMargin": "9.83137400",
                "totalMaintenanceMargin": "0.41568700",
                "totalMarginBalance": "23.03235621",
                "totalOpenOrderInitialMargin": "9.00000000",
                "totalPositionInitialMargin": "0.83137400",
                "totalUnrealizedProfit": "0.03219710",
                "totalWalletBalance": "22.15879444",
                "asset": "USDT",
                "subAccountList":[
                    {
                        "email": "123@test.com",
                        "totalInitialMargin": "9.00000000",
                        "totalMaintenanceMargin": "0.00000000",
                        "totalMarginBalance": "22.12659734",
                        "totalOpenOrderInitialMargin": "9.00000000",
                        "totalPositionInitialMargin": "0.00000000",
                        "totalUnrealizedProfit": "0.00000000",
                        "totalWalletBalance": "22.12659734",
                        "asset": "USDT"
                    },
                    {
                        "email": "345@test.com",
                        "totalInitialMargin": "0.83137400",
                        "totalMaintenanceMargin": "0.41568700",
                        "totalMarginBalance": "0.90575887",
                        "totalOpenOrderInitialMargin": "0.00000000",
                        "totalPositionInitialMargin": "0.83137400",
                        "totalUnrealizedProfit": "0.03219710",
                        "totalWalletBalance": "0.87356177",
                        "asset": "USDT"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/futures/accountSummary', True, data=params)

    def get_subaccount_futures_positionrisk(self, **params):
        """Get Futures Position-Risk of Sub-account (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#get-futures-position-risk-of-sub-account-for-master-account

        :param email: required - Sub account email
        :type email: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "entryPrice": "9975.12000",
                    "leverage": "50",              // current initial leverage
                    "maxNotional": "1000000",      // notional value limit of current initial leverage
                    "liquidationPrice": "7963.54",
                    "markPrice": "9973.50770517",
                    "positionAmount": "0.010",
                    "symbol": "BTCUSDT",
                    "unrealizedProfit": "-0.01612295"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/futures/positionRisk', True, data=params)

    def make_subaccount_futures_transfer(self, **params):
        """Futures Transfer for Sub-account (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#futures-transfer-for-sub-account-for-master-account

        :param email: required - Sub account email
        :type email: str
        :param asset: required - The asset being transferred, e.g., USDT
        :type asset: str
        :param amount: required - The amount to be transferred
        :type amount: float
        :param type: required - 1: transfer from subaccount's spot account to its USDT-margined futures account
                                2: transfer from subaccount's USDT-margined futures account to its spot account
                                3: transfer from subaccount's spot account to its COIN-margined futures account
                                4: transfer from subaccount's COIN-margined futures account to its spot account
        :type type: int

        :returns: API response

        .. code-block:: python

            {
                "txnId":"2966662589"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'sub-account/futures/transfer', True, data=params)

    def make_subaccount_margin_transfer(self, **params):
        """Margin Transfer for Sub-account (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#margin-transfer-for-sub-account-for-master-account

        :param email: required - Sub account email
        :type email: str
        :param asset: required - The asset being transferred, e.g., USDT
        :type asset: str
        :param amount: required - The amount to be transferred
        :type amount: float
        :param type: required - 1: transfer from subaccount's spot account to margin account
                                2: transfer from subaccount's margin account to its spot account
        :type type: int

        :returns: API response

        .. code-block:: python

            {
                "txnId":"2966662589"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'sub-account/margin/transfer', True, data=params)

    def make_subaccount_to_subaccount_transfer(self, **params):
        """Transfer to Sub-account of Same Master (For Sub-account)

        https://binance-docs.github.io/apidocs/spot/en/#transfer-to-sub-account-of-same-master-for-sub-account

        :param toEmail: required - Sub account email
        :type toEmail: str
        :param asset: required - The asset being transferred, e.g., USDT
        :type asset: str
        :param amount: required - The amount to be transferred
        :type amount: float
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "txnId":"2966662589"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'sub-account/transfer/subToSub', True, data=params)

    def make_subaccount_to_master_transfer(self, **params):
        """Transfer to Master (For Sub-account)

        https://binance-docs.github.io/apidocs/spot/en/#transfer-to-master-for-sub-account

        :param asset: required - The asset being transferred, e.g., USDT
        :type asset: str
        :param amount: required - The amount to be transferred
        :type amount: float
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "txnId":"2966662589"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'sub-account/transfer/subToMaster', True, data=params)

    def get_subaccount_transfer_history(self, **params):
        """Sub-account Transfer History (For Sub-account)

        https://binance-docs.github.io/apidocs/spot/en/#transfer-to-master-for-sub-account

        :param asset: required - The asset being transferred, e.g., USDT
        :type asset: str
        :param type: optional - 1: transfer in, 2: transfer out
        :type type: int
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param limit: optional - Default 500
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
              {
                "counterParty":"master",
                "email":"master@test.com",
                "type":1,  // 1 for transfer in, 2 for transfer out
                "asset":"BTC",
                "qty":"1",
                "status":"SUCCESS",
                "tranId":11798835829,
                "time":1544433325000
              },
              {
                "counterParty":"subAccount",
                "email":"sub2@test.com",
                "type":2,
                "asset":"ETH",
                "qty":"2",
                "status":"SUCCESS",
                "tranId":11798829519,
                "time":1544433326000
              }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/transfer/subUserHistory', True, data=params)

    def make_universal_transfer_sa(self, **params):
        """Universal Transfer (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#universal-transfer-for-master-account

        :param fromEmail: optional
        :type fromEmail: str
        :param toEmail: optional
        :type toEmail: str
        :param fromAccountType: required
        :type fromAccountType: str
        :param toAccountType: required
        :type toAccountType: str
        :param asset: required - The asset being transferred, e.g., USDT
        :type asset: str
        :param amount: required
        :type amount: float
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "tranId":11945860693
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'sub-account/universalTransfer', True, data=params)

    def get_universal_transfer_history(self, **params):
        """Universal Transfer (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#query-universal-transfer-history

        :param fromEmail: optional
        :type fromEmail: str
        :param toEmail: optional
        :type toEmail: str
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param page: optional
        :type page: int
        :param limit: optional
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
              {
                "tranId":11945860693,
                "fromEmail":"master@test.com",
                "toEmail":"subaccount1@test.com",
                "asset":"BTC",
                "amount":"0.1",
                "fromAccountType":"SPOT",
                "toAccountType":"COIN_FUTURE",
                "status":"SUCCESS",
                "createTimeStamp":1544433325000
              },
              {
                "tranId":11945857955,
                "fromEmail":"master@test.com",
                "toEmail":"subaccount2@test.com",
                "asset":"ETH",
                "amount":"0.2",
                "fromAccountType":"SPOT",
                "toAccountType":"USDT_FUTURE",
                "status":"SUCCESS",
                "createTimeStamp":1544433326000
              }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/universalTransfer', True, data=params)

    # Futures API
    def futures_stream_get_listen_key(self):
        res = self._request_futures_api('post', 'listenKey', signed=False, data={})
        return res['listenKey']

    def futures_stream_keepalive(self, listenKey):
        params = {
            'listenKey': listenKey
        }
        return self._request_futures_api('put', 'listenKey', signed=False, data=params)

    def futures_stream_close(self, listenKey):
        
        params = {
            'listenKey': listenKey
        }
        return self._request_futures_api('delete', 'listenKey', signed=False, data=params)

    def futures_ping(self):
        """Test connectivity to the Rest API

        https://binance-docs.github.io/apidocs/futures/en/#test-connectivity

        """
        return self._request_futures_api('get', 'ping')

    def futures_time(self):
        """Test connectivity to the Rest API and get the current server time.

        https://binance-docs.github.io/apidocs/futures/en/#check-server-time

        """
        return self._request_futures_api('get', 'time')

    def futures_exchange_info(self):
        """Current exchange trading rules and symbol information

        https://binance-docs.github.io/apidocs/futures/en/#exchange-information-market_data

        """
        return self._request_futures_api('get', 'exchangeInfo')

    def futures_order_book(self, **params):
        """Get the Order Book for the market

        https://binance-docs.github.io/apidocs/futures/en/#order-book-market_data

        """
        return self._request_futures_api('get', 'depth', data=params)

    def futures_recent_trades(self, **params):
        """Get recent trades (up to last 500).

        https://binance-docs.github.io/apidocs/futures/en/#recent-trades-list-market_data

        """
        return self._request_futures_api('get', 'trades', data=params)

    def futures_historical_trades(self, **params):
        """Get older market historical trades.

        https://binance-docs.github.io/apidocs/futures/en/#old-trades-lookup-market_data

        """
        return self._request_futures_api('get', 'historicalTrades', data=params)

    def futures_aggregate_trades(self, **params):
        """Get compressed, aggregate trades. Trades that fill at the time, from the same order, with the same
        price will have the quantity aggregated.

        https://binance-docs.github.io/apidocs/futures/en/#compressed-aggregate-trades-list-market_data

        """
        return self._request_futures_api('get', 'aggTrades', data=params)

    def futures_klines(self, **params):
        """Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.

        https://binance-docs.github.io/apidocs/futures/en/#kline-candlestick-data-market_data

        """
        return self._request_futures_api('get', 'klines', data=params)
    
    def futures_continous_klines(self, **params):
        """Kline/candlestick bars for a specific contract type. Klines are uniquely identified by their open time.

        https://binance-docs.github.io/apidocs/futures/en/#continuous-contract-kline-candlestick-data

        """
        return self._request_futures_api('get', 'continuousKlines', data=params)

    def futures_historical_klines(self, symbol, interval, start_str, end_str=None,
                           limit=500):
        """Get historical futures klines from Binance

        :param symbol: Name of symbol pair e.g BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param start_str: Start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: str|int
        :param limit: Default 500; max 1000.
        :type limit: int

        :return: list of OHLCV values

        """
        return self._historical_klines(symbol, interval, start_str, end_str=None, limit=500, spot=False)

    def futures_historical_klines_generator(self, symbol, interval, start_str, end_str=None):
        """Get historical futures klines generator from Binance

        :param symbol: Name of symbol pair e.g BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param start_str: Start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: str|int

        :return: generator of OHLCV values

        """

        return self._historical_klines_generator(symbol, interval, start_str, end_str=end_str, spot=False)

    def futures_mark_price(self, **params):
        """Get Mark Price and Funding Rate

        https://binance-docs.github.io/apidocs/futures/en/#mark-price-market_data

        """
        return self._request_futures_api('get', 'premiumIndex', data=params)

    def futures_funding_rate(self, **params):
        """Get funding rate history

        https://binance-docs.github.io/apidocs/futures/en/#get-funding-rate-history-market_data

        """
        return self._request_futures_api('get', 'fundingRate', data=params)

    def futures_ticker(self, **params):
        """24 hour rolling window price change statistics.

        https://binance-docs.github.io/apidocs/futures/en/#24hr-ticker-price-change-statistics-market_data

        """
        return self._request_futures_api('get', 'ticker/24hr', data=params)

    def futures_symbol_ticker(self, **params):
        """Latest price for a symbol or symbols.

        https://binance-docs.github.io/apidocs/futures/en/#symbol-price-ticker-market_data

        """
        return self._request_futures_api('get', 'ticker/price', data=params)

    def futures_orderbook_ticker(self, **params):
        """Best price/qty on the order book for a symbol or symbols.

        https://binance-docs.github.io/apidocs/futures/en/#symbol-order-book-ticker-market_data

        """
        return self._request_futures_api('get', 'ticker/bookTicker', data=params)

    def futures_liquidation_orders(self, **params):
        """Get all liquidation orders

        https://binance-docs.github.io/apidocs/futures/en/#get-all-liquidation-orders-market_data

        """
        return self._request_futures_api('get', 'ticker/allForceOrders', data=params)

    def futures_open_interest(self, **params):
        """Get present open interest of a specific symbol.

        https://binance-docs.github.io/apidocs/futures/en/#open-interest-market_data

        """
        return self._request_futures_api('get', 'ticker/openInterest', data=params)
    # TODO
    def futures_topLongShortAccountRatio(self, **params):
        return self._request_futures_data_api('get', 'topLongShortAccountRatio', data=params)
    
    def futures_topLongShortPositionRatio(self, **params):
        return self._request_futures_data_api('get', 'topLongShortPositionRatio', data=params)
    
    def futures_globalLongShortAccountRatio(self, **params):
        return self._request_futures_data_api('get', 'globalLongShortAccountRatio', data=params)
    
    def futures_takerlongshortRatio(self, **params):
        return self._request_futures_data_api('get', 'takerlongshortRatio', data=params)
    
    def futures_open_interest_hist(self, **params):
        """Get open interest statistics of a specific symbol.

        https://binance-docs.github.io/apidocs/futures/en/#open-interest-statistics

        """
        return self._request_futures_data_api('get', 'openInterestHist', data=params)

    def futures_leverage_bracket(self, **params):
        """Notional and Leverage Brackets

        https://binance-docs.github.io/apidocs/futures/en/#notional-and-leverage-brackets-market_data

        """
        return self._request_futures_api('get', 'leverageBracket', True, data=params)

    def futures_account_transfer(self, **params):
        """Execute transfer between spot account and futures account.

        https://binance-docs.github.io/apidocs/futures/en/#new-future-account-transfer

        """
        return self._request_margin_api('post', 'futures/transfer', True, data=params)

    def transfer_history(self, **params):
        """Get future account transaction history list

        https://binance-docs.github.io/apidocs/futures/en/#get-future-account-transaction-history-list-user_data

        """
        return self._request_margin_api('get', 'futures/transfer', True, data=params)

    def futures_create_order(self, **params):
        """Send in a new order.

        https://binance-docs.github.io/apidocs/futures/en/#new-order-trade

        """
        return self._request_futures_api('post', 'order', True, data=params)

    def futures_get_order(self, **params):
        """Check an order's status.

        https://binance-docs.github.io/apidocs/futures/en/#query-order-user_data

        """
        return self._request_futures_api('get', 'order', True, data=params)

    def futures_get_open_orders(self, **params):
        """Get all open orders on a symbol.

        https://binance-docs.github.io/apidocs/futures/en/#current-open-orders-user_data

        """
        return self._request_futures_api('get', 'openOrders', True, data=params)

    def futures_get_all_orders(self, **params):
        """Get all futures account orders; active, canceled, or filled.

        https://binance-docs.github.io/apidocs/futures/en/#all-orders-user_data

        """
        return self._request_futures_api('get', 'allOrders', True, data=params)

    def futures_cancel_order(self, **params):
        """Cancel an active futures order.

        https://binance-docs.github.io/apidocs/futures/en/#cancel-order-trade

        """
        return self._request_futures_api('delete', 'order', True, data=params)

    def futures_cancel_all_open_orders(self, **params):
        """Cancel all open futures orders

        https://binance-docs.github.io/apidocs/futures/en/#cancel-all-open-orders-trade

        """
        return self._request_futures_api('delete', 'allOpenOrders', True, data=params)

    def futures_cancel_orders(self, **params):
        """Cancel multiple futures orders

        https://binance-docs.github.io/apidocs/futures/en/#cancel-multiple-orders-trade

        """
        return self._request_futures_api('delete', 'batchOrders', True, data=params)

    def futures_account_balance(self, version=2, **params):
        """Get futures account balance

        https://binance-docs.github.io/apidocs/futures/en/#future-account-balance-user_data

        """
        return self._request_futures_api('get', 'balance', True, version, data=params)

    def futures_account(self, **params):
        """Get current account information.

        https://binance-docs.github.io/apidocs/futures/en/#account-information-user_data

        """
        return self._request_futures_api('get', 'account', True, data=params)

    def futures_change_leverage(self, **params):
        """Change user's initial leverage of specific symbol market

        https://binance-docs.github.io/apidocs/futures/en/#change-initial-leverage-trade

        """
        return self._request_futures_api('post', 'leverage', True, data=params)

    def futures_change_margin_type(self, **params):
        """Change the margin type for a symbol

        https://binance-docs.github.io/apidocs/futures/en/#change-margin-type-trade

        """
        return self._request_futures_api('post', 'marginType', True, data=params)

    def futures_change_position_margin(self, **params):
        """Change the position margin for a symbol

        https://binance-docs.github.io/apidocs/futures/en/#modify-isolated-position-margin-trade

        """
        return self._request_futures_api('post', 'positionMargin', True, data=params)

    def futures_position_margin_history(self, **params):
        """Get position margin change history

        https://binance-docs.github.io/apidocs/futures/en/#get-postion-margin-change-history-trade

        """
        return self._request_futures_api('get', 'positionMargin/history', True, data=params)

    def futures_position_information(self, **params):
        """Get position information

        https://binance-docs.github.io/apidocs/futures/en/#position-information-user_data

        """
        return self._request_futures_api('get', 'positionRisk', True, data=params)

    def futures_account_trades(self, **params):
        """Get trades for the authenticated account and symbol.

        https://binance-docs.github.io/apidocs/futures/en/#account-trade-list-user_data

        """
        return self._request_futures_api('get', 'userTrades', True, data=params)

    def futures_income_history(self, **params):
        """Get income history for authenticated account

        https://binance-docs.github.io/apidocs/futures/en/#get-income-history-user_data

        """
        return self._request_futures_api('get', 'income', True, data=params)

    def futures_change_position_mode(self, **params):
        """Change position mode for authenticated account

        https://binance-docs.github.io/apidocs/futures/en/#change-position-mode-trade
        
        """
        return self._request_futures_api('post', 'positionSide/dual', True, data=params)

    def futures_get_position_mode(self, **params):
        """Get position mode for authenticated account

        https://binance-docs.github.io/apidocs/futures/en/#get-current-position-mode-user_data
        
        """
        return self._request_futures_api('get', 'positionSide/dual', True, data=params)

    # COIN Futures API
    def futures_coin_ping(self):
        """Test connectivity to the Rest API

        https://binance-docs.github.io/apidocs/delivery/en/#test-connectivity

        """
        return self._request_futures_coin_api("get", "ping")

    def futures_coin_time(self):
        """Test connectivity to the Rest API and get the current server time.

        https://binance-docs.github.io/apidocs/delivery/en/#check-server-time

        """
        return self._request_futures_coin_api("get", "time")

    def futures_coin_exchange_info(self):
        """Current exchange trading rules and symbol information

        https://binance-docs.github.io/apidocs/delivery/en/#exchange-information

        """
        return self._request_futures_coin_api("get", "exchangeInfo")

    def futures_coin_order_book(self, **params):
        """Get the Order Book for the market

        https://binance-docs.github.io/apidocs/delivery/en/#order-book

        """
        return self._request_futures_coin_api("get", "depth", data=params)

    def futures_coin_recent_trades(self, **params):
        """Get recent trades (up to last 500).

        https://binance-docs.github.io/apidocs/delivery/en/#recent-trades-list

        """
        return self._request_futures_coin_api("get", "trades", data=params)

    def futures_coin_historical_trades(self, **params):
        """Get older market historical trades.

        https://binance-docs.github.io/apidocs/delivery/en/#old-trades-lookup-market_data

        """
        return self._request_futures_coin_api("get", "historicalTrades", data=params)

    def futures_coin_aggregate_trades(self, **params):
        """Get compressed, aggregate trades. Trades that fill at the time, from the same order, with the same
        price will have the quantity aggregated.

        https://binance-docs.github.io/apidocs/delivery/en/#compressed-aggregate-trades-list

        """
        return self._request_futures_coin_api("get", "aggTrades", data=params)

    def futures_coin_klines(self, **params):
        """Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.

        https://binance-docs.github.io/apidocs/delivery/en/#kline-candlestick-data

        """
        return self._request_futures_coin_api("get", "klines", data=params)

    def futures_coin_continous_klines(self, **params):
        """Kline/candlestick bars for a specific contract type. Klines are uniquely identified by their open time.

        https://binance-docs.github.io/apidocs/delivery/en/#continuous-contract-kline-candlestick-data

        """
        return self._request_futures_coin_api("get", "continuousKlines", data=params)

    def futures_coin_index_price_klines(self, **params):
        """Kline/candlestick bars for the index price of a pair..

        https://binance-docs.github.io/apidocs/delivery/en/#index-price-kline-candlestick-data

        """
        return self._request_futures_coin_api("get", "indexPriceKlines", data=params)

    def futures_coin_mark_price_klines(self, **params):
        """Kline/candlestick bars for the index price of a pair..

        https://binance-docs.github.io/apidocs/delivery/en/#mark-price-kline-candlestick-data

        """
        return self._request_futures_coin_api("get", "markPriceKlines", data=params)

    def futures_coin_mark_price(self, **params):
        """Get Mark Price and Funding Rate

        https://binance-docs.github.io/apidocs/delivery/en/#index-price-and-mark-price

        """
        return self._request_futures_coin_api("get", "premiumIndex", data=params)

    def futures_coin_funding_rate(self, **params):
        """Get funding rate history

        https://binance-docs.github.io/apidocs/delivery/en/#get-funding-rate-history-of-perpetual-futures

        """
        return self._request_futures_coin_api("get", "fundingRate", data=params)

    def futures_coin_ticker(self, **params):
        """24 hour rolling window price change statistics.

        https://binance-docs.github.io/apidocs/delivery/en/#24hr-ticker-price-change-statistics

        """
        return self._request_futures_coin_api("get", "ticker/24hr", data=params)

    def futures_coin_symbol_ticker(self, **params):
        """Latest price for a symbol or symbols.

        https://binance-docs.github.io/apidocs/delivery/en/#symbol-price-ticker

        """
        return self._request_futures_coin_api("get", "ticker/price", data=params)

    def futures_coin_orderbook_ticker(self, **params):
        """Best price/qty on the order book for a symbol or symbols.

        https://binance-docs.github.io/apidocs/delivery/en/#symbol-order-book-ticker

        """
        return self._request_futures_coin_api("get", "ticker/bookTicker", data=params)

    def futures_coin_liquidation_orders(self, **params):
        """Get all liquidation orders

        https://binance-docs.github.io/apidocs/delivery/en/#get-all-liquidation-orders

        """
        return self._request_futures_coin_api("get", "allForceOrders", data=params)

    def futures_coin_open_interest(self, **params):
        """Get present open interest of a specific symbol.

        https://binance-docs.github.io/apidocs/delivery/en/#open-interest

        """
        return self._request_futures_coin_api("get", "openInterest", data=params)

    def futures_coin_open_interest_hist(self, **params):
        """Get open interest statistics of a specific symbol.

        https://binance-docs.github.io/apidocs/delivery/en/#open-interest-statistics-market-data

        """
        return self._request_futures_coin_data_api("get", "openInterestHist", data=params)

    def futures_coin_leverage_bracket(self, **params):
        """Notional and Leverage Brackets

        https://binance-docs.github.io/apidocs/delivery/en/#notional-bracket-for-pair-user_data

        """
        return self._request_futures_coin_api(
            "get", "leverageBracket", version=2, signed=True, data=params
        )

    def new_transfer_history(self, **params):
        """Get future account transaction history list

        https://binance-docs.github.io/apidocs/delivery/en/#new-future-account-transfer

        """
        return self._request_margin_api("get", "asset/transfer", True, data=params)
        # return self._request_margin_api("get", "futures/transfer", True, data=params)

    def universal_transfer(self, **params):
        """Unviversal transfer api accross different binance account types

        https://binance-docs.github.io/apidocs/spot/en/#user-universal-transfer
        """
        return self._request_margin_api(
            "post", "asset/transfer", signed=True, data=params
        )

    def futures_coin_create_order(self, **params):
        """Send in a new order.

        https://binance-docs.github.io/apidocs/delivery/en/#new-order-trade

        """
        return self._request_futures_coin_api("post", "order", True, data=params)

    def futures_coin_get_order(self, **params):
        """Check an order's status.

        https://binance-docs.github.io/apidocs/delivery/en/#query-order-user_data

        """
        return self._request_futures_coin_api("get", "order", True, data=params)

    def futures_coin_get_open_orders(self, **params):
        """Get all open orders on a symbol.

        https://binance-docs.github.io/apidocs/delivery/en/#current-all-open-orders-user_data

        """
        return self._request_futures_coin_api("get", "openOrders", True, data=params)

    def futures_coin_get_all_orders(self, **params):
        """Get all futures account orders; active, canceled, or filled.

        https://binance-docs.github.io/apidocs/delivery/en/#all-orders-user_data

        """
        return self._request_futures_coin_api(
            "get", "allOrders", signed=True, data=params
        )

    def futures_coin_cancel_order(self, **params):
        """Cancel an active futures order.

        https://binance-docs.github.io/apidocs/delivery/en/#cancel-order-trade

        """
        return self._request_futures_coin_api(
            "delete", "order", signed=True, data=params
        )

    def futures_coin_cancel_all_open_orders(self, **params):
        """Cancel all open futures orders

        https://binance-docs.github.io/apidocs/delivery/en/#cancel-all-open-orders-trade

        """
        return self._request_futures_coin_api(
            "delete", "allOpenOrders", signed=True, data=params
        )

    def futures_coin_cancel_orders(self, **params):
        """Cancel multiple futures orders

        https://binance-docs.github.io/apidocs/delivery/en/#cancel-multiple-orders-trade

        """
        return self._request_futures_coin_api(
            "delete", "batchOrders", True, data=params
        )

    def futures_coin_account_balance(self, **params):
        """Get futures account balance

        https://binance-docs.github.io/apidocs/delivery/en/#futures-account-balance-user_data

        """
        return self._request_futures_coin_api(
            "get", "balance", signed=True, data=params
        )

    def futures_coin_account(self, **params):
        """Get current account information.

        https://binance-docs.github.io/apidocs/delivery/en/#account-information-user_data

        """
        return self._request_futures_coin_api(
            "get", "account", signed=True, data=params
        )

    def futures_coin_change_leverage(self, **params):
        """Change user's initial leverage of specific symbol market

        https://binance-docs.github.io/apidocs/delivery/en/#change-initial-leverage-trade

        """
        return self._request_futures_coin_api(
            "post", "leverage", signed=True, data=params
        )

    def futures_coin_change_margin_type(self, **params):
        """Change the margin type for a symbol

        https://binance-docs.github.io/apidocs/delivery/en/#change-margin-type-trade

        """
        return self._request_futures_coin_api(
            "post", "marginType", signed=True, data=params
        )

    def futures_coin_change_position_margin(self, **params):
        """Change the position margin for a symbol

        https://binance-docs.github.io/apidocs/delivery/en/#modify-isolated-position-margin-trade

        """
        return self._request_futures_coin_api(
            "post", "positionMargin", True, data=params
        )

    def futures_coin_position_margin_history(self, **params):
        """Get position margin change history

        https://binance-docs.github.io/apidocs/delivery/en/#get-position-margin-change-history-trade

        """
        return self._request_futures_coin_api(
            "get", "positionMargin/history", True, data=params
        )

    def futures_coin_position_information(self, **params):
        """Get position information

        https://binance-docs.github.io/apidocs/delivery/en/#position-information-user_data

        """
        return self._request_futures_coin_api("get", "positionRisk", True, data=params)

    def futures_coin_account_trades(self, **params):
        """Get trades for the authenticated account and symbol.

        https://binance-docs.github.io/apidocs/delivery/en/#account-trade-list-user_data

        """
        return self._request_futures_coin_api("get", "userTrades", True, data=params)

    def futures_coin_income_history(self, **params):
        """Get income history for authenticated account

        https://binance-docs.github.io/apidocs/delivery/en/#get-income-history-user_data

        """
        return self._request_futures_coin_api("get", "income", True, data=params)

    def futures_coin_change_position_mode(self, **params):
        """Change user's position mode (Hedge Mode or One-way Mode ) on EVERY symbol

        https://binance-docs.github.io/apidocs/delivery/en/#change-position-mode-trade
        """
        return self._request_futures_coin_api("post", "positionSide/dual", True, data=params)
    
    def futures_coin_get_position_mode(self, **params):
        """Get user's position mode (Hedge Mode or One-way Mode ) on EVERY symbol

        https://binance-docs.github.io/apidocs/delivery/en/#get-current-position-mode-user_data

        """
        return self._request_futures_coin_api("get", "positionSide/dual", True, data=params)

    def get_all_coins_info(self, **params):
        """Get information of coins (available for deposit and withdraw) for user.

        https://binance-docs.github.io/apidocs/spot/en/#all-coins-39-information-user_data

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "coin": "BTC",
                "depositAllEnable": true,
                "withdrawAllEnable": true,
                "name": "Bitcoin",
                "free": "0",
                "locked": "0",
                "freeze": "0",
                "withdrawing": "0",
                "ipoing": "0",
                "ipoable": "0",
                "storage": "0",
                "isLegalMoney": false,
                "trading": true,
                "networkList": [
                    {
                        "network": "BNB",
                        "coin": "BTC",
                        "withdrawIntegerMultiple": "0.00000001",
                        "isDefault": false,
                        "depositEnable": true,
                        "withdrawEnable": true,
                        "depositDesc": "",
                        "withdrawDesc": "",
                        "specialTips": "Both a MEMO and an Address are required to successfully deposit your BEP2-BTCB tokens to Binance.",
                        "name": "BEP2",
                        "resetAddressStatus": false,
                        "addressRegex": "^(bnb1)[0-9a-z]{38}$",
                        "memoRegex": "^[0-9A-Za-z-_]{1,120}$",
                        "withdrawFee": "0.0000026",
                        "withdrawMin": "0.0000052",
                        "withdrawMax": "0",
                        "minConfirm": 1,
                        "unLockConfirm": 0
                    },
                    {
                        "network": "BTC",
                        "coin": "BTC",
                        "withdrawIntegerMultiple": "0.00000001",
                        "isDefault": true,
                        "depositEnable": true,
                        "withdrawEnable": true,
                        "depositDesc": "",
                        "withdrawDesc": "",
                        "specialTips": "",
                        "name": "BTC",
                        "resetAddressStatus": false,
                        "addressRegex": "^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^(bc1)[0-9A-Za-z]{39,59}$",
                        "memoRegex": "",
                        "withdrawFee": "0.0005",
                        "withdrawMin": "0.001",
                        "withdrawMax": "0",
                        "minConfirm": 1,
                        "unLockConfirm": 2
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'capital/config/getall', True, data=params)

    def get_account_snapshot(self, **params):
        """Get daily account snapshot of specific type.

        https://binance-docs.github.io/apidocs/spot/en/#daily-account-snapshot-user_data

        :param type: required. Valid values are SPOT/MARGIN/FUTURES.
        :type type: string
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param limit: optional
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
               "code":200, // 200 for success; others are error codes
               "msg":"", // error message
               "snapshotVos":[
                  {
                     "data":{
                        "balances":[
                           {
                              "asset":"BTC",
                              "free":"0.09905021",
                              "locked":"0.00000000"
                           },
                           {
                              "asset":"USDT",
                              "free":"1.89109409",
                              "locked":"0.00000000"
                           }
                        ],
                        "totalAssetOfBtc":"0.09942700"
                     },
                     "type":"spot",
                     "updateTime":1576281599000
                  }
               ]
            }

        OR

        .. code-block:: python

            {
               "code":200, // 200 for success; others are error codes
               "msg":"", // error message
               "snapshotVos":[
                  {
                     "data":{
                        "marginLevel":"2748.02909813",
                        "totalAssetOfBtc":"0.00274803",
                        "totalLiabilityOfBtc":"0.00000100",
                        "totalNetAssetOfBtc":"0.00274750",
                        "userAssets":[
                           {
                              "asset":"XRP",
                              "borrowed":"0.00000000",
                              "free":"1.00000000",
                              "interest":"0.00000000",
                              "locked":"0.00000000",
                              "netAsset":"1.00000000"
                           }
                        ]
                     },
                     "type":"margin",
                     "updateTime":1576281599000
                  }
               ]
            }

        OR

        .. code-block:: python

            {
               "code":200, // 200 for success; others are error codes
               "msg":"", // error message
               "snapshotVos":[
                  {
                     "data":{
                        "assets":[
                           {
                              "asset":"USDT",
                              "marginBalance":"118.99782335",
                              "walletBalance":"120.23811389"
                           }
                        ],
                        "position":[
                           {
                              "entryPrice":"7130.41000000",
                              "markPrice":"7257.66239673",
                              "positionAmt":"0.01000000",
                              "symbol":"BTCUSDT",
                              "unRealizedProfit":"1.24029054"
                           }
                        ]
                     },
                     "type":"futures",
                     "updateTime":1576281599000
                  }
               ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'accountSnapshot', True, data=params)

    def disable_fast_withdraw_switch(self, **params):
        """Disable Fast Withdraw Switch

        https://binance-docs.github.io/apidocs/spot/en/#disable-fast-withdraw-switch-user_data

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'disableFastWithdrawSwitch', True, data=params)

    def enable_fast_withdraw_switch(self, **params):
        """Enable Fast Withdraw Switch

        https://binance-docs.github.io/apidocs/spot/en/#enable-fast-withdraw-switch-user_data

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'enableFastWithdrawSwitch', True, data=params)

    """
    ====================================================================================================================
    Options API
    ====================================================================================================================
    """
    # Quoting interface endpoints

    def options_ping(self):
        """Test connectivity

        https://binance-docs.github.io/apidocs/voptions/en/#test-connectivity

        """
        return self._request_options_api('get', 'ping')

    def options_time(self):
        """Get server time

        https://binance-docs.github.io/apidocs/voptions/en/#get-server-time

        """
        return self._request_options_api('get', 'time')

    def options_info(self):
        """Get current trading pair info

        https://binance-docs.github.io/apidocs/voptions/en/#get-current-trading-pair-info

        """
        return self._request_options_api('get', 'optionInfo')

    def options_exchange_info(self):
        """Get current limit info and trading pair info

        https://binance-docs.github.io/apidocs/voptions/en/#get-current-limit-info-and-trading-pair-info

        """
        return self._request_options_api('get', 'exchangeInfo')

    def options_index_price(self, **params):
        """Get the spot index price

        https://binance-docs.github.io/apidocs/voptions/en/#get-the-spot-index-price

        :param underlying: required - Spot pair（Option contract underlying asset）- BTCUSDT
        :type underlying: str

        """
        return self._request_options_api('get', 'index', data=params)

    def options_price(self, **params):
        """Get the latest price

        https://binance-docs.github.io/apidocs/voptions/en/#get-the-latest-price

        :param symbol: optional - Option trading pair - BTC-200730-9000-C
        :type symbol: str

        """
        return self._request_options_api('get', 'ticker', data=params)

    def options_mark_price(self, **params):
        """Get the latest mark price

        https://binance-docs.github.io/apidocs/voptions/en/#get-the-latest-mark-price

        :param symbol: optional - Option trading pair - BTC-200730-9000-C
        :type symbol: str

        """
        return self._request_options_api('get', 'mark', data=params)

    def options_order_book(self, **params):
        """Depth information

        https://binance-docs.github.io/apidocs/voptions/en/#depth-information

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param limit: optional - Default:100 Max:1000.Optional value:[10, 20, 50, 100, 500, 1000] - 100
        :type limit: int

        """
        return self._request_options_api('get', 'depth', data=params)

    def options_klines(self, **params):
        """Candle data

        https://binance-docs.github.io/apidocs/voptions/en/#candle-data

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param interval: required - Time interval - 5m
        :type interval: str
        :param startTime: optional - Start Time - 1592317127349
        :type startTime: int
        :param endTime: optional - End Time - 1592317127349
        :type endTime: int
        :param limit: optional - Number of records Default:500 Max:1500 - 500
        :type limit: int

        """
        return self._request_options_api('get', 'klines', data=params)

    def options_recent_trades(self, **params):
        """Recently completed Option trades

        https://binance-docs.github.io/apidocs/voptions/en/#recently-completed-option-trades

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param limit: optional - Number of records Default:100 Max:500 - 100
        :type limit: int

        """
        return self._request_options_api('get', 'trades', data=params)

    def options_historical_trades(self, **params):
        """Query trade history

        https://binance-docs.github.io/apidocs/voptions/en/#query-trade-history

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param fromId: optional - The deal ID from which to return. The latest deal record is returned by default - 1592317127349
        :type fromId: int
        :param limit: optional - Number of records Default:100 Max:500 - 100
        :type limit: int

        """
        return self._request_options_api('get', 'historicalTrades', data=params)

    # Account and trading interface endpoints

    def options_account_info(self, **params):
        """Account asset info (USER_DATA)

        https://binance-docs.github.io/apidocs/voptions/en/#account-asset-info-user_data

        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('get', 'account', signed=True, data=params)

    def options_funds_transfer(self, **params):
        """Funds transfer (USER_DATA)

        https://binance-docs.github.io/apidocs/voptions/en/#funds-transfer-user_data

        :param currency: required - Asset type - USDT
        :type currency: str
        :param type: required - IN: Transfer from spot account to option account OUT: Transfer from option account to spot account - IN
        :type type: str (ENUM)
        :param amount: required - Amount - 10000
        :type amount: float
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('post', 'transfer', signed=True, data=params)

    def options_positions(self, **params):
        """Option holdings info (USER_DATA)

        https://binance-docs.github.io/apidocs/voptions/en/#option-holdings-info-user_data

        :param symbol: optional - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('get', 'position', signed=True, data=params)

    def options_bill(self, **params):
        """Account funding flow (USER_DATA)

        https://binance-docs.github.io/apidocs/voptions/en/#account-funding-flow-user_data

        :param currency: required - Asset type - USDT
        :type currency: str
        :param recordId: optional - Return the recordId and subsequent data, the latest data is returned by default - 100000
        :type recordId: int
        :param startTime: optional - Start Time - 1593511200000
        :type startTime: int
        :param endTime: optional - End Time - 1593511200000
        :type endTime: int
        :param limit: optional - Number of result sets returned Default:100 Max:1000 - 100
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('post', 'bill', signed=True, data=params)

    def options_place_order(self, **params):
        """Option order (TRADE)

        https://binance-docs.github.io/apidocs/voptions/en/#option-order-trade

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param side: required - Buy/sell direction: SELL, BUY - BUY
        :type side: str (ENUM)
        :param type: required - Order Type: LIMIT, MARKET - LIMIT
        :type type: str (ENUM)
        :param quantity: required - Order Quantity - 3
        :type quantity: float
        :param price: optional - Order Price - 1000
        :type price: float
        :param timeInForce: optional - Time in force method（Default GTC) - GTC
        :type timeInForce: str (ENUM)
        :param reduceOnly: optional - Reduce Only (Default false) - false
        :type reduceOnly: bool
        :param postOnly: optional - Post Only (Default false) - false
        :type postOnly: bool
        :param newOrderRespType: optional - "ACK", "RESULT", Default "ACK" - ACK
        :type newOrderRespType: str (ENUM)
        :param clientOrderId: optional - User-defined order ID cannot be repeated in pending orders - 10000
        :type clientOrderId: str
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('post', 'order', signed=True, data=params)

    def options_place_batch_order(self, **params):
        """Place Multiple Option orders (TRADE)

        https://binance-docs.github.io/apidocs/voptions/en/#place-multiple-option-orders-trade

        :param orders: required - order list. Max 5 orders - [{"symbol":"BTC-210115-35000-C","price":"100","quantity":"0.0001","side":"BUY","type":"LIMIT"}]
        :type orders: list
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('post', 'batchOrders', signed=True, data=params)

    def options_cancel_order(self, **params):
        """Cancel Option order (TRADE)

        https://binance-docs.github.io/apidocs/voptions/en/#cancel-option-order-trade

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param orderId: optional - Order ID - 4611875134427365377
        :type orderId: str
        :param clientOrderId: optional - User-defined order ID - 10000
        :type clientOrderId: str
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('delete', 'order', signed=True, data=params)

    def options_cancel_batch_order(self, **params):
        """Cancel Multiple Option orders (TRADE)

        https://binance-docs.github.io/apidocs/voptions/en/#cancel-multiple-option-orders-trade

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param orderIds: optional - Order ID - [4611875134427365377,4611875134427365378]
        :type orderId: list
        :param clientOrderIds: optional - User-defined order ID - ["my_id_1","my_id_2"]
        :type clientOrderIds: list
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('delete', 'batchOrders', signed=True, data=params)

    def options_cancel_all_orders(self, **params):
        """Cancel all Option orders (TRADE)

        https://binance-docs.github.io/apidocs/voptions/en/#cancel-all-option-orders-trade

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('delete', 'allOpenOrders', signed=True, data=params)

    def options_query_order(self, **params):
        """Query Option order (TRADE)

        https://binance-docs.github.io/apidocs/voptions/en/#query-option-order-trade

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param orderId: optional - Order ID - 4611875134427365377
        :type orderId: str
        :param clientOrderId: optional - User-defined order ID - 10000
        :type clientOrderId: str
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('get', 'order', signed=True, data=params)

    def options_query_pending_orders(self, **params):
        """Query current pending Option orders (TRADE)

        https://binance-docs.github.io/apidocs/voptions/en/#query-current-pending-option-orders-trade

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param orderId: optional - Returns the orderId and subsequent orders, the most recent order is returned by default - 100000
        :type orderId: str
        :param startTime: optional - Start Time - 1593511200000
        :type startTime: int
        :param endTime: optional - End Time - 1593511200000
        :type endTime: int
        :param limit: optional - Number of result sets returned Default:100 Max:1000 - 100
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('get', 'openOrders', signed=True, data=params)

    def options_query_order_history(self, **params):
        """Query Option order history (TRADE)

        https://binance-docs.github.io/apidocs/voptions/en/#query-option-order-history-trade

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param orderId: optional - Returns the orderId and subsequent orders, the most recent order is returned by default - 100000
        :type orderId: str
        :param startTime: optional - Start Time - 1593511200000
        :type startTime: int
        :param endTime: optional - End Time - 1593511200000
        :type endTime: int
        :param limit: optional - Number of result sets returned Default:100 Max:1000 - 100
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('get', 'historyOrders', signed=True, data=params)

    def options_user_trades(self, **params):
        """Option Trade List (USER_DATA)

        https://binance-docs.github.io/apidocs/voptions/en/#option-trade-list-user_data

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param fromId: optional - Trade id to fetch from. Default gets most recent trades. - 4611875134427365376
        :type orderId: int
        :param startTime: optional - Start Time - 1593511200000
        :type startTime: int
        :param endTime: optional - End Time - 1593511200000
        :type endTime: int
        :param limit: optional - Number of result sets returned Default:100 Max:1000 - 100
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('get', 'userTrades', signed=True, data=params)
#%%
class BinanceClientProtocol(WebSocketClientProtocol):
    def __init__(self):
        super(WebSocketClientProtocol, self).__init__()
    def onConnect(self, response):
        # reset the delay after reconnecting
        self.factory.resetDelay()
    def onMessage(self, payload, isBinary):
        if isBinary:
            try:
                payload = gzip.decompress(payload)
            except:
                print('Could not interpret binary response payload')
                return
        try:
            payload_obj = json.loads(payload.decode('utf8'))
        except ValueError:
            pass
        else:
            self.factory.callback(payload_obj)

class BinanceReconnectingClientFactory(ReconnectingClientFactory):
    # set initial delay to a short time
    initialDelay = 0.1
    maxDelay = 10
    maxRetries = 5

class BinanceClientFactory(WebSocketClientFactory, BinanceReconnectingClientFactory):
    protocol = BinanceClientProtocol
    _reconnect_error_payload = {
        'e': 'error',
        'm': 'Max reconnect retries reached'
    }
    def clientConnectionFailed(self, connector, reason):
        self.retry(connector)
        if self.retries > self.maxRetries:
            self.callback(self._reconnect_error_payload)
    def clientConnectionLost(self, connector, reason):
        self.retry(connector)
        if self.retries > self.maxRetries:
            self.callback(self._reconnect_error_payload)

class BinanceSocketManager(threading.Thread):
    STREAM_URL = 'wss://stream.binance.com:9443/'
    FSTREAM_URL = 'wss://fstream.binance.com/'
    VSTREAM_URL = 'wss://vstream.binance.com/'
    VSTREAM_TESTNET_URL = 'wss://testnetws.binanceops.com/'

    WEBSOCKET_DEPTH_5 = '5'
    WEBSOCKET_DEPTH_10 = '10'
    WEBSOCKET_DEPTH_20 = '20'

    DEFAULT_USER_TIMEOUT = 30 * 60  # 30 minutes

    def __init__(self, client, user_timeout=DEFAULT_USER_TIMEOUT):
        """Initialise the BinanceSocketManager

        :param client: Binance API client
        :type client: binance.Client
        :param user_timeout: Custom websocket timeout
        :type user_timeout: int

        """
        threading.Thread.__init__(self)
        self._conns = {}
        self._client = client
        self._user_timeout = user_timeout
        self._timers = {'user': None, 'margin': None}
        self._listen_keys = {'user': None, 'margin': None}
        self._account_callbacks = {'user': None, 'margin': None}
        # Isolated margin sockets will be opened under the 'symbol' name
        self.testnet = self._client.testnet

    def _start_socket(self, path, callback, prefix='ws/'):
        if path in self._conns:
            return False

        factory_url = self.STREAM_URL + prefix + path
        factory = BinanceClientFactory(factory_url)
        factory.protocol = BinanceClientProtocol
        factory.callback = callback
        factory.reconnect = True
        if factory.host.startswith('testnet.binance'):
            context_factory = ssl.optionsForClientTLS(factory.host)
        else:
            context_factory = ssl.ClientContextFactory()

        self._conns[path] = connectWS(factory, context_factory)
        return path

    def _start_futures_socket(self, path, callback, prefix='stream?streams='):
        if path in self._conns:
            return False

        factory_url = self.FSTREAM_URL + prefix + path
        factory = BinanceClientFactory(factory_url)
        factory.protocol = BinanceClientProtocol
        factory.callback = callback
        factory.reconnect = True
        context_factory = ssl.ClientContextFactory()

        self._conns[path] = connectWS(factory, context_factory)
        return path

    def _start_options_socket(self, path, callback, prefix='ws/'):
        if path in self._conns:
            return False

        if self.testnet:
            url = self.VSTREAM_TESTNET_URL
        else:
            url = self.VSTREAM_URL

        factory_url = url + prefix + path
        factory = BinanceClientFactory(factory_url)
        factory.protocol = BinanceClientProtocol
        factory.callback = callback
        factory.reconnect = True
        context_factory = ssl.ClientContextFactory()

        self._conns[path] = connectWS(factory, context_factory)
        return path

    def start_depth_socket(self, symbol, callback, depth=None, interval=None):
        """Start a websocket for symbol market depth returning either a diff or a partial book

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#partial-book-depth-streams

        :param symbol: required
        :type symbol: str
        :param callback: callback function to handle messages
        :type callback: function
        :param depth: optional Number of depth entries to return, default None. If passed returns a partial book instead of a diff
        :type depth: str
        :param interval: optional interval for updates, default None. If not set, updates happen every second. Must be 0, None (1s) or 100 (100ms)
        :type interval: int

        :returns: connection key string if successful, False otherwise

        Partial Message Format

        .. code-block:: python

            {
                "lastUpdateId": 160,  # Last update ID
                "bids": [             # Bids to be updated
                    [
                        "0.0024",     # price level to be updated
                        "10",         # quantity
                        []            # ignore
                    ]
                ],
                "asks": [             # Asks to be updated
                    [
                        "0.0026",     # price level to be updated
                        "100",        # quantity
                        []            # ignore
                    ]
                ]
            }


        Diff Message Format

        .. code-block:: python

            {
                "e": "depthUpdate", # Event type
                "E": 123456789,     # Event time
                "s": "BNBBTC",      # Symbol
                "U": 157,           # First update ID in event
                "u": 160,           # Final update ID in event
                "b": [              # Bids to be updated
                    [
                        "0.0024",   # price level to be updated
                        "10",       # quantity
                        []          # ignore
                    ]
                ],
                "a": [              # Asks to be updated
                    [
                        "0.0026",   # price level to be updated
                        "100",      # quantity
                        []          # ignore
                    ]
                ]
            }

        """
        socket_name = symbol.lower() + '@depth'
        if depth and depth != '1':
            socket_name = '{}{}'.format(socket_name, depth)
        if interval:
            if interval in [0, 100]:
                socket_name = '{}@{}ms'.format(socket_name, interval)
            else:
                raise ValueError("Websocket interval value not allowed. Allowed values are [0, 100]")
        return self._start_socket(socket_name, callback)

    def start_kline_socket(self, symbol, callback, interval=Client.KLINE_INTERVAL_1MINUTE):
        """Start a websocket for symbol kline data

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#klinecandlestick-streams

        :param symbol: required
        :type symbol: str
        :param callback: callback function to handle messages
        :type callback: function
        :param interval: Kline interval, default KLINE_INTERVAL_1MINUTE
        :type interval: str

        :returns: connection key string if successful, False otherwise

        Message Format

        .. code-block:: python

            {
                "e": "kline",					# event type
                "E": 1499404907056,				# event time
                "s": "ETHBTC",					# symbol
                "k": {
                    "t": 1499404860000, 		# start time of this bar
                    "T": 1499404919999, 		# end time of this bar
                    "s": "ETHBTC",				# symbol
                    "i": "1m",					# interval
                    "f": 77462,					# first trade id
                    "L": 77465,					# last trade id
                    "o": "0.10278577",			# open
                    "c": "0.10278645",			# close
                    "h": "0.10278712",			# high
                    "l": "0.10278518",			# low
                    "v": "17.47929838",			# volume
                    "n": 4,						# number of trades
                    "x": false,					# whether this bar is final
                    "q": "1.79662878",			# quote volume
                    "V": "2.34879839",			# volume of active buy
                    "Q": "0.24142166",			# quote volume of active buy
                    "B": "13279784.01349473"	# can be ignored
                    }
            }
        """
        socket_name = '{}@kline_{}'.format(symbol.lower(), interval)
        return self._start_socket(socket_name, callback)

    def start_miniticker_socket(self, callback, update_time=1000):
        """Start a miniticker websocket for all trades

        This is not in the official Binance api docs, but this is what
        feeds the right column on a ticker page on Binance.

        :param callback: callback function to handle messages
        :type callback: function
        :param update_time: time between callbacks in milliseconds, must be 1000 or greater
        :type update_time: int

        :returns: connection key string if successful, False otherwise

        Message Format

        .. code-block:: python

            [
                {
                    'e': '24hrMiniTicker',  # Event type
                    'E': 1515906156273,     # Event time
                    's': 'QTUMETH',         # Symbol
                    'c': '0.03836900',      # close
                    'o': '0.03953500',      # open
                    'h': '0.04400000',      # high
                    'l': '0.03756000',      # low
                    'v': '147435.80000000', # volume
                    'q': '5903.84338533'    # quote volume
                }
            ]
        """

        return self._start_socket('!miniTicker@arr@{}ms'.format(update_time), callback)

    def start_trade_socket(self, symbol, callback):
        """Start a websocket for symbol trade data

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#trade-streams

        :param symbol: required
        :type symbol: str
        :param callback: callback function to handle messages
        :type callback: function

        :returns: connection key string if successful, False otherwise

        Message Format

        .. code-block:: python

            {
                "e": "trade",     # Event type
                "E": 123456789,   # Event time
                "s": "BNBBTC",    # Symbol
                "t": 12345,       # Trade ID
                "p": "0.001",     # Price
                "q": "100",       # Quantity
                "b": 88,          # Buyer order Id
                "a": 50,          # Seller order Id
                "T": 123456785,   # Trade time
                "m": true,        # Is the buyer the market maker?
                "M": true         # Ignore.
            }

        """
        return self._start_socket(symbol.lower() + '@trade', callback)

    def start_aggtrade_socket(self, symbol, callback):
        """Start a websocket for symbol trade data

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#aggregate-trade-streams

        :param symbol: required
        :type symbol: str
        :param callback: callback function to handle messages
        :type callback: function

        :returns: connection key string if successful, False otherwise

        Message Format

        .. code-block:: python

            {
                "e": "aggTrade",		# event type
                "E": 1499405254326,		# event time
                "s": "ETHBTC",			# symbol
                "a": 70232,				# aggregated tradeid
                "p": "0.10281118",		# price
                "q": "8.15632997",		# quantity
                "f": 77489,				# first breakdown trade id
                "l": 77489,				# last breakdown trade id
                "T": 1499405254324,		# trade time
                "m": false,				# whether buyer is a maker
                "M": true				# can be ignored
            }

        """
        return self._start_socket(symbol.lower() + '@aggTrade', callback)

    def start_aggtrade_futures_socket(self, symbol, callback):
        """Start a websocket for aggregate symbol trade data for the futures stream

        :param symbol: required
        :type symbol: str
        :param callback: callback function to handle messages
        :type callback: function

        :returns: connection key string if successful, False otherwise

        Message Format

        .. code-block:: python

            {
                "e": "aggTrade",  // Event type
                "E": 123456789,   // Event time
                "s": "BTCUSDT",    // Symbol
                "a": 5933014,     // Aggregate trade ID
                "p": "0.001",     // Price
                "q": "100",       // Quantity
                "f": 100,         // First trade ID
                "l": 105,         // Last trade ID
                "T": 123456785,   // Trade time
                "m": true,        // Is the buyer the market maker?
            }

        """
        return self._start_futures_socket(symbol.lower() + '@aggTrade', callback)

    def start_symbol_ticker_socket(self, symbol, callback):
        """Start a websocket for a symbol's ticker data

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#individual-symbol-ticker-streams

        :param symbol: required
        :type symbol: str
        :param callback: callback function to handle messages
        :type callback: function

        :returns: connection key string if successful, False otherwise

        Message Format

        .. code-block:: python

            {
                "e": "24hrTicker",  # Event type
                "E": 123456789,     # Event time
                "s": "BNBBTC",      # Symbol
                "p": "0.0015",      # Price change
                "P": "250.00",      # Price change percent
                "w": "0.0018",      # Weighted average price
                "x": "0.0009",      # Previous day's close price
                "c": "0.0025",      # Current day's close price
                "Q": "10",          # Close trade's quantity
                "b": "0.0024",      # Best bid price
                "B": "10",          # Bid bid quantity
                "a": "0.0026",      # Best ask price
                "A": "100",         # Best ask quantity
                "o": "0.0010",      # Open price
                "h": "0.0025",      # High price
                "l": "0.0010",      # Low price
                "v": "10000",       # Total traded base asset volume
                "q": "18",          # Total traded quote asset volume
                "O": 0,             # Statistics open time
                "C": 86400000,      # Statistics close time
                "F": 0,             # First trade ID
                "L": 18150,         # Last trade Id
                "n": 18151          # Total number of trades
            }

        """
        return self._start_socket(symbol.lower() + '@ticker', callback)

    def start_ticker_socket(self, callback):
        """Start a websocket for all ticker data

        By default all markets are included in an array.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#all-market-tickers-stream

        :param callback: callback function to handle messages
        :type callback: function

        :returns: connection key string if successful, False otherwise

        Message Format

        .. code-block:: python

            [
                {
                    'F': 278610,
                    'o': '0.07393000',
                    's': 'BCCBTC',
                    'C': 1509622420916,
                    'b': '0.07800800',
                    'l': '0.07160300',
                    'h': '0.08199900',
                    'L': 287722,
                    'P': '6.694',
                    'Q': '0.10000000',
                    'q': '1202.67106335',
                    'p': '0.00494900',
                    'O': 1509536020916,
                    'a': '0.07887800',
                    'n': 9113,
                    'B': '1.00000000',
                    'c': '0.07887900',
                    'x': '0.07399600',
                    'w': '0.07639068',
                    'A': '2.41900000',
                    'v': '15743.68900000'
                }
            ]
        """
        return self._start_socket('!ticker@arr', callback)

    def start_symbol_mark_price_socket(self, symbol, callback, fast=True):
        """Start a websocket for a symbol's futures mark price
        https://binance-docs.github.io/apidocs/futures/en/#mark-price-stream
        :param symbol: required
        :type symbol: str
        :param callback: callback function to handle messages
        :type callback: function
        :returns: connection key string if successful, False otherwise
        Message Format
        .. code-block:: python
            {
                "e": "markPriceUpdate",  // Event type
                "E": 1562305380000,      // Event time
                "s": "BTCUSDT",          // Symbol
                "p": "11185.87786614",   // Mark price
                "r": "0.00030000",       // Funding rate
                "T": 1562306400000       // Next funding time
            }
        """
        stream_name = '@markPrice@1s' if fast else '@markPrice'
        return self._start_futures_socket(symbol.lower() + stream_name, callback)

    def start_all_mark_price_socket(self, callback, fast=True):
        """Start a websocket for all futures mark price data
        By default all symbols are included in an array.
        https://binance-docs.github.io/apidocs/futures/en/#mark-price-stream-for-all-market
        :param callback: callback function to handle messages
        :type callback: function
        :returns: connection key string if successful, False otherwise
        Message Format
        .. code-block:: python

            [
                {
                    "e": "markPriceUpdate",  // Event type
                    "E": 1562305380000,      // Event time
                    "s": "BTCUSDT",          // Symbol
                    "p": "11185.87786614",   // Mark price
                    "r": "0.00030000",       // Funding rate
                    "T": 1562306400000       // Next funding time
                }
            ]
        """
        stream_name = '!markPrice@arr@1s' if fast else '!markPrice@arr'
        return self._start_futures_socket(stream_name, callback)

    def start_symbol_ticker_futures_socket(self, symbol, callback):
        """Start a websocket for a symbol's ticker data
        By default all markets are included in an array.
        https://binance-docs.github.io/apidocs/futures/en/#individual-symbol-book-ticker-streams
        :param symbol: required
        :type symbol: str
        :param callback: callback function to handle messages
        :type callback: function
        :returns: connection key string if successful, False otherwise
        .. code-block:: python
            [
                {
                  "u":400900217,     // order book updateId
                  "s":"BNBUSDT",     // symbol
                  "b":"25.35190000", // best bid price
                  "B":"31.21000000", // best bid qty
                  "a":"25.36520000", // best ask price
                  "A":"40.66000000"  // best ask qty
                }
            ]
        """
        return self._start_futures_socket(symbol.lower() + '@bookTicker', callback)
    
    def start_individual_symbol_ticker_futures_socket(self, symbol, callback):
        """Start a futures websocket for a single symbol's ticker data
        https://binance-docs.github.io/apidocs/futures/en/#individual-symbol-ticker-streams
        :param symbol: required
        :type symbol: str
        :param callback: callback function to handle messages
        :type callback: function
        :returns: connection key string if successful, False otherwise
        .. code-block:: python
            {
                "e": "24hrTicker",  // Event type
                "E": 123456789,     // Event time
                "s": "BTCUSDT",     // Symbol
                "p": "0.0015",      // Price change
            }
        """
        return self._start_futures_socket(symbol.lower() + '@ticker', callback)

    def start_all_ticker_futures_socket(self, callback):
        """Start a websocket for all ticker data
        By default all markets are included in an array.
        https://binance-docs.github.io/apidocs/futures/en/#all-book-tickers-stream
        :param callback: callback function to handle messages
        :type callback: function
        :returns: connection key string if successful, False otherwise
        Message Format
        .. code-block:: python
            [
                {
                  "u":400900217,     // order book updateId
                  "s":"BNBUSDT",     // symbol
                  "b":"25.35190000", // best bid price
                  "B":"31.21000000", // best bid qty
                  "a":"25.36520000", // best ask price
                  "A":"40.66000000"  // best ask qty
                }
            ]
        """


        return self._start_futures_socket('!bookTicker', callback)

    def start_symbol_book_ticker_socket(self, symbol, callback):
        """Start a websocket for the best bid or ask's price or quantity for a specified symbol.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#individual-symbol-book-ticker-streams

        :param symbol: required
        :type symbol: str
        :param callback: callback function to handle messages
        :type callback: function

        :returns: connection key string if successful, False otherwise

        Message Format

        .. code-block:: python

            {
                "u":400900217,     // order book updateId
                "s":"BNBUSDT",     // symbol
                "b":"25.35190000", // best bid price
                "B":"31.21000000", // best bid qty
                "a":"25.36520000", // best ask price
                "A":"40.66000000"  // best ask qty
            }

        """
        return self._start_socket(symbol.lower() + '@bookTicker', callback)

    def start_book_ticker_socket(self, callback):
        """Start a websocket for the best bid or ask's price or quantity for all symbols.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#all-book-tickers-stream

        :param callback: callback function to handle messages
        :type callback: function

        :returns: connection key string if successful, False otherwise

        Message Format

        .. code-block:: python

            {
                // Same as <symbol>@bookTicker payload
            }

        """
        return self._start_socket('!bookTicker', callback)

    def start_multiplex_socket(self, streams, callback):
        """Start a multiplexed socket using a list of socket names.
        User stream sockets can not be included.

        Symbols in socket name must be lowercase i.e bnbbtc@aggTrade, neobtc@ticker

        Combined stream events are wrapped as follows: {"stream":"<streamName>","data":<rawPayload>}

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md

        :param streams: list of stream names in lower case
        :type streams: list
        :param callback: callback function to handle messages
        :type callback: function

        :returns: connection key string if successful, False otherwise

        Message Format - see Binance API docs for all types

        """
        stream_path = 'streams={}'.format('/'.join(streams))
        return self._start_socket(stream_path, callback, 'stream?')

    def start_options_multiplex_socket(self, streams, callback):
        """Start a multiplexed socket using a list of socket names.
        User stream sockets can not be included.

        Symbols in socket name must be lowercase i.e bnbbtc@aggTrade, neobtc@ticker

        Combined stream events are wrapped as follows: {"stream":"<streamName>","data":<rawPayload>}

        https://binance-docs.github.io/apidocs/voptions/en/#account-and-trading-interface

        :param streams: list of stream names in lower case
        :type streams: list
        :param callback: callback function to handle messages
        :type callback: function

        :returns: connection key string if successful, False otherwise

        Message Format - see Binance API docs for all types

        """
        stream_path = 'streams={}'.format('/'.join([s.lower() for s in streams]))
        return self._start_options_socket(stream_path, callback, 'stream?')

    def start_user_socket(self, callback): # TODO
        """Start a websocket for user data
        https://github.com/binance-exchange/binance-official-api-docs/blob/master/user-data-stream.md
        https://binance-docs.github.io/apidocs/spot/en/#listen-key-spot
        :param callback: callback function to handle messages
        :type callback: function
        :returns: connection key string if successful, False otherwise
        Message Format - see Binance API docs for all types
        """
        # Get the user listen key
        user_listen_key = self._client.stream_get_listen_key()
        # and start the socket with this specific key
        return self._start_account_socket('user', user_listen_key, callback)
    
    def start_futures_user_socket(self, callback):
        """Start a websocket for user data
        https://github.com/binance-exchange/binance-official-api-docs/blob/master/user-data-stream.md
        https://binance-docs.github.io/apidocs/spot/en/#listen-key-spot
        :param callback: callback function to handle messages
        :type callback: function
        :returns: connection key string if successful, False otherwise
        Message Format - see Binance API docs for all types
        """
        # Get the user listen key
        user_listen_key = self._client.futures_stream_get_listen_key()
        # and start the socket with this specific key
        return self._start_account_futures_socket('futures', user_listen_key, callback)
    
    def start_margin_socket(self, callback):
        """Start a websocket for cross-margin data

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-margin

        :param callback: callback function to handle messages
        :type callback: function

        :returns: connection key string if successful, False otherwise

        Message Format - see Binance API docs for all types
        """
        # Get the user margin listen key
        margin_listen_key = self._client.margin_stream_get_listen_key()
        # and start the socket with this specific key
        return self._start_account_socket('margin', margin_listen_key, callback)

    def start_isolated_margin_socket(self, symbol, callback):
        """Start a websocket for isolated margin data

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-isolated-margin

        :param symbol: required - symbol for the isolated margin account
        :type symbol: str
        :param callback: callback function to handle messages
        :type callback: function

        :returns: connection key string if successful, False otherwise

        Message Format - see Binance API docs for all types
        """
        # Get the isolated margin listen key
        isolated_margin_listen_key = self._client.isolated_margin_stream_get_listen_key(symbol)
        # and start the socket with this specific kek
        return self._start_account_socket(symbol, isolated_margin_listen_key, callback)

    def start_options_ticker_socket(self, symbol, callback):
        """Subscribe to a 24 hour ticker info stream

        https://binance-docs.github.io/apidocs/voptions/en/#market-streams-payload-24-hour-ticker

        :param symbol: required
        :type symbol: str
        :param callback: callback function to handle messages
        :type callback: function
        """
        return self._start_options_socket(symbol.lower() + '@ticker', callback)

    def start_options_recent_trades_socket(self, symbol, callback):
        """Subscribe to a latest completed trades stream

        https://binance-docs.github.io/apidocs/voptions/en/#market-streams-payload-latest-completed-trades

        :param symbol: required
        :type symbol: str
        :param callback: callback function to handle messages
        :type callback: function
        """
        return self._start_options_socket(symbol.lower() + '@trade', callback)

    def start_options_kline_socket(self, symbol, callback, interval=Client.KLINE_INTERVAL_1MINUTE):
        """Subscribe to a candlestick data stream

        https://binance-docs.github.io/apidocs/voptions/en/#market-streams-payload-candle

        :param symbol: required
        :type symbol: str
        :param callback: callback function to handle messages
        :type callback: function
        :param interval: Kline interval, default KLINE_INTERVAL_1MINUTE
        :type interval: str
        """
        return self._start_options_socket(symbol.lower() + '@kline_' + interval, callback)

    def start_options_depth_socket(self, symbol, callback, depth='10'):
        """Subscribe to a depth data stream

        https://binance-docs.github.io/apidocs/voptions/en/#market-streams-payload-depth

        :param symbol: required
        :type symbol: str
        :param callback: callback function to handle messages
        :type callback: function
        :param depth: optional Number of depth entries to return, default 10.
        :type depth: str
        """
        return self._start_options_socket(symbol.lower() + '@depth' + str(depth), callback)

    def _start_account_socket(self, socket_type, listen_key, callback):
        """Starts one of user or margin socket"""
        self._check_account_socket_open(listen_key)
        self._listen_keys[socket_type] = listen_key
        self._account_callbacks[socket_type] = callback
        conn_key = self._start_socket(listen_key, callback)
        if conn_key:
            # start timer to keep socket alive
            self._start_socket_timer(socket_type)
        return conn_key

    def _start_account_futures_socket(self, socket_type, listen_key, callback):
        """Starts futures account socket"""
        self._check_account_socket_open(listen_key)
        self._listen_keys[socket_type] = listen_key
        self._account_callbacks[socket_type] = callback
        conn_key = self._start_futures_socket(listen_key, callback, "ws/")
        if conn_key:
            # start timer to keep socket alive
            self._start_socket_timer(socket_type)
        return conn_key
    
    def _check_account_socket_open(self, listen_key):
        if not listen_key:
            return
        for conn_key in self._conns:
            if len(conn_key) >= 60 and conn_key[:60] == listen_key:
                self.stop_socket(conn_key)
                break

    def _start_socket_timer(self, socket_type):
        callback = self._keepalive_account_socket
        self._timers[socket_type] = threading.Timer(self._user_timeout, callback, [socket_type])
        self._timers[socket_type].setDaemon(True)
        self._timers[socket_type].start()

    def _keepalive_account_socket(self, socket_type):
        if socket_type == 'user':
            callback = self._account_callbacks[socket_type]
            listen_key = self._client.stream_get_listen_key()
        elif socket_type == 'margin':  # cross-margin
            callback = self._account_callbacks[socket_type]
            listen_key = self._client.margin_stream_get_listen_key()
        elif socket_type == 'futures':
            listen_key_func = self._client.futures_stream_get_listen_key
            callback = self._account_callbacks[socket_type]
            listen_key = listen_key_func()
        else:  # isolated margin
            callback = self._account_callbacks.get(socket_type, None)
            listen_key = self._client.isolated_margin_stream_get_listen_key(socket_type)  # Passing symbol for isolated margin
        
        if listen_key != self._listen_keys[socket_type]:
            self._start_account_socket(socket_type, listen_key, callback)
        else:
            if socket_type == 'user':
                self._client.stream_keepalive(listen_key)
            elif socket_type == 'margin':  # cross-margin
                self._client.margin_stream_keepalive(listen_key)
            elif socket_type == 'futures':  # cross-margin
                self._client.futures_stream_keepalive(listen_key)
            else:  # isolated margin
                self._client.isolated_margin_stream_keepalive(socket_type, listen_key)  # Passing symbol for isolated margin
            self._start_socket_timer(socket_type)

    def stop_socket(self, conn_key):
        """Stop a websocket given the connection key

        :param conn_key: Socket connection key
        :type conn_key: string

        :returns: connection key string if successful, False otherwise
        """
        if conn_key not in self._conns:
            return

        # disable reconnecting if we are closing
        self._conns[conn_key].factory = WebSocketClientFactory(self.STREAM_URL + 'tmp_path')
        self._conns[conn_key].disconnect()
        del(self._conns[conn_key])

        # OBSOLETE - removed when adding isolated margin.  Loop over keys instead
        # # check if we have a user stream socket
        # if len(conn_key) >= 60 and conn_key[:60] == self._listen_keys['user']:
        #     self._stop_account_socket('user')

        # # or a margin stream socket
        # if len(conn_key) >= 60 and conn_key[:60] == self._listen_keys['margin']:
        #     self._stop_account_socket('margin')

        # NEW - Loop over keys in _listen_keys dictionary to find a match on
        # user, cross-margin and isolated margin:
        for key, value in self._listen_keys.items():
            if len(conn_key) >= 60 and conn_key[:60] == value:
                self._stop_account_socket(key)


    def _stop_account_socket(self, socket_type):
        if not self._listen_keys.get(socket_type, None):
            return
        if self._timers.get(socket_type, None):
            self._timers[socket_type].cancel()
            self._timers[socket_type] = None
        self._listen_keys[socket_type] = None

    def run(self):
        try:
            reactor.run(installSignalHandlers=False)
        except ReactorAlreadyRunning:
            # Ignore error about reactor already running
            pass

    def close(self):
        """Close all connections
        """
        keys = set(self._conns.keys())
        for key in keys:
            self.stop_socket(key)
        self._conns = {}

#%%
# def date_to_milliseconds(date_str):
#     """Convert UTC date to milliseconds

#     If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

#     See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/

#     :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
#     :type date_str: str
#     """
#     # get epoch value in UTC
#     epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
#     # parse our date string
#     d = dateparser.parse(date_str)
#     # if the date is not timezone aware apply UTC timezone
#     if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
#         d = d.replace(tzinfo=pytz.utc)

#     # return the difference in time
#     return int((d - epoch).total_seconds() * 1000.0)


def interval_to_milliseconds(interval):
    """Convert a Binance interval string to milliseconds

    :param interval: Binance interval string, e.g.: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w
    :type interval: str

    :return:
         int value of interval in milliseconds
         None if interval prefix is not a decimal integer
         None if interval suffix is not one of m, h, d, w

    """
    seconds_per_unit = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60,
    }
    try:
        return int(interval[:-1]) * seconds_per_unit[interval[-1]] * 1000
    except (ValueError, KeyError):
        return None
#%%
class BinanceAPIException(Exception):

    def __init__(self, response):
        self.code = 0
        try:
            json_res = response.json()
        except ValueError:
            self.message = 'Invalid JSON error message from Binance: {}'.format(response.text)
        else:
            self.code = json_res['code']
            self.message = json_res['msg']
        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):  # pragma: no cover
        return 'APIError(code=%s): %s' % (self.code, self.message)


class BinanceRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'BinanceRequestException: %s' % self.message


class BinanceOrderException(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return 'BinanceOrderException(code=%s): %s' % (self.code, self.message)


class BinanceOrderMinAmountException(BinanceOrderException):

    def __init__(self, value):
        message = "Amount must be a multiple of %s" % value
        super(BinanceOrderMinAmountException, self).__init__(-1013, message)


class BinanceOrderMinPriceException(BinanceOrderException):

    def __init__(self, value):
        message = "Price must be at least %s" % value
        super(BinanceOrderMinPriceException, self).__init__(-1013, message)


class BinanceOrderMinTotalException(BinanceOrderException):

    def __init__(self, value):
        message = "Total must be at least %s" % value
        super(BinanceOrderMinTotalException, self).__init__(-1013, message)


class BinanceOrderUnknownSymbolException(BinanceOrderException):

    def __init__(self, value):
        message = "Unknown symbol %s" % value
        super(BinanceOrderUnknownSymbolException, self).__init__(-1013, message)


class BinanceOrderInactiveSymbolException(BinanceOrderException):

    def __init__(self, value):
        message = "Attempting to trade an inactive symbol %s" % value
        super(BinanceOrderInactiveSymbolException, self).__init__(-1013, message)


class BinanceWithdrawException(Exception):
    def __init__(self, message):
        if message == u'参数异常':
            message = 'Withdraw to this address through the website first'
        self.message = message

    def __str__(self):
        return 'BinanceWithdrawException: %s' % self.message
#%%
class DepthCache(object):

    def __init__(self, symbol):
        """Initialise the DepthCache

        :param symbol: Symbol to create depth cache for
        :type symbol: string

        """
        self.symbol = symbol
        self._bids = {}
        self._asks = {}
        self.update_time = None

    def add_bid(self, bid):
        """Add a bid to the cache

        :param bid:
        :return:

        """
        self._bids[bid[0]] = float(bid[1])
        if bid[1] == "0.00000000":
            del self._bids[bid[0]]

    def add_ask(self, ask):
        """Add an ask to the cache

        :param ask:
        :return:

        """
        self._asks[ask[0]] = float(ask[1])
        if ask[1] == "0.00000000":
            del self._asks[ask[0]]

    def get_bids(self):
        """Get the current bids

        :return: list of bids with price and quantity as floats

        .. code-block:: python

            [
                [
                    0.0001946,  # Price
                    45.0        # Quantity
                ],
                [
                    0.00019459,
                    2384.0
                ],
                [
                    0.00019158,
                    5219.0
                ],
                [
                    0.00019157,
                    1180.0
                ],
                [
                    0.00019082,
                    287.0
                ]
            ]

        """
        return DepthCache.sort_depth(self._bids, reverse=True)

    def get_asks(self):
        """Get the current asks

        :return: list of asks with price and quantity as floats

        .. code-block:: python

            [
                [
                    0.0001955,  # Price
                    57.0'       # Quantity
                ],
                [
                    0.00019699,
                    778.0
                ],
                [
                    0.000197,
                    64.0
                ],
                [
                    0.00019709,
                    1130.0
                ],
                [
                    0.0001971,
                    385.0
                ]
            ]

        """
        return DepthCache.sort_depth(self._asks, reverse=False)

    @staticmethod
    def sort_depth(vals, reverse=False):
        """Sort bids or asks by price
        """
        lst = [[float(price), quantity] for price, quantity in vals.items()]
        lst = sorted(lst, key=itemgetter(0), reverse=reverse)
        return lst


class BaseDepthCacheManager(object):
    DEFAULT_REFRESH = 60 * 30  # 30 minutes

    def __init__(self, client, symbol, callback=None, refresh_interval=None, bm=None, limit=10):
        """Initialise the DepthCacheManager

        :param client: Binance API client
        :type client: binance.Client
        :param symbol: Symbol to create depth cache for
        :type symbol: string
        :param callback: Optional function to receive depth cache updates
        :type callback: function
        :param refresh_interval: Optional number of seconds between cache refresh, use 0 or None to disable
        :type refresh_interval: int
        :param limit: Optional number of orders to get from orderbook
        :type limit: int

        """
        self._client = client
        self._symbol = symbol
        self._limit = limit
        self._callback = callback
        self._last_update_id = None
        self._depth_message_buffer = []
        self._bm = bm
        self._refresh_interval = refresh_interval or self.DEFAULT_REFRESH
        self._conn_key = None

        self._start_socket()
        self._init_cache()

    def _init_cache(self):
        """Initialise the depth cache and set a refresh time

        :return:
        """

        # initialise or clear depth cache
        self._depth_cache = DepthCache(self._symbol)

        # set a time to refresh the depth cache
        if self._refresh_interval:
            self._refresh_time = int(time.time()) + self._refresh_interval

    def _start_socket(self):
        """Start the depth cache socket

        :return:
        """
        if self._bm is None:
            self._bm = BinanceSocketManager(self._client)

        self._conn_key = self._get_conn_key()
        if not self._bm.is_alive():
            self._bm.start()

    def _get_conn_key(self):
        raise NotImplementedError

    def _depth_event(self, msg):
        """Handle a depth event

        :param msg:
        :return:

        """

        if 'e' in msg and msg['e'] == 'error':
            # close the socket
            self.close()

            # notify the user by returning a None value
            if self._callback:
                self._callback(None)

        self._process_depth_message(msg)

    def _process_depth_message(self, msg, buffer=False):
        """Process a depth event message.

        :param msg: Depth event message.
        :return:

        """

        # add any bid or ask values
        for bid in msg['b']:
            self._depth_cache.add_bid(bid)
        for ask in msg['a']:
            self._depth_cache.add_ask(ask)

        # keeping update time
        self._depth_cache.update_time = msg['E']

        # call the callback with the updated depth cache
        if self._callback:
            self._callback(self._depth_cache)

        # after processing event see if we need to refresh the depth cache
        if self._refresh_interval and int(time.time()) > self._refresh_time:
            self.close()
            self._init_cache()
            self._start_socket()

    def get_depth_cache(self):
        """Get the current depth cache

        :return: DepthCache object

        """
        return self._depth_cache

    def close(self, close_socket=False):
        """Close the open socket for this manager

        :return:
        """
        self._bm.stop_socket(self._conn_key)
        if close_socket:
            self._bm.close()
        time.sleep(1)
        self._depth_cache = None

    def get_symbol(self):
        """Get the symbol

        :return: symbol
        """
        return self._symbol


class DepthCacheManager(BaseDepthCacheManager):

    def __init__(self, client, symbol, callback=None, refresh_interval=None, bm=None, limit=500,
                 ws_interval=None):
        """Initialise the DepthCacheManager

        :param client: Binance API client
        :type client: binance.Client
        :param symbol: Symbol to create depth cache for
        :type symbol: string
        :param callback: Optional function to receive depth cache updates
        :type callback: function
        :param refresh_interval: Optional number of seconds between cache refresh, use 0 or None to disable
        :type refresh_interval: int
        :param limit: Optional number of orders to get from orderbook
        :type limit: int
        :param ws_interval: Optional interval for updates on websocket, default None. If not set, updates happen every second. Must be 0, None (1s) or 100 (100ms).
        :type ws_interval: int

        """
        self._ws_interval = ws_interval
        self._last_update_id = None
        self._depth_message_buffer = []
        super().__init__(client, symbol, callback, refresh_interval, bm, limit)

    def _init_cache(self):
        """Initialise the depth cache calling REST endpoint

        :return:
        """
        self._last_update_id = None
        self._depth_message_buffer = []

        res = self._client.get_order_book(symbol=self._symbol, limit=self._limit)

        # initialise or clear depth cache
        super()._init_cache()

        # process bid and asks from the order book
        for bid in res['bids']:
            self._depth_cache.add_bid(bid)
        for ask in res['asks']:
            self._depth_cache.add_ask(ask)

        # set first update id
        self._last_update_id = res['lastUpdateId']

        # Apply any updates from the websocket
        for msg in self._depth_message_buffer:
            self._process_depth_message(msg, buffer=True)

        # clear the depth buffer
        self._depth_message_buffer = []

    def _start_socket(self):
        """Start the depth cache socket

        :return:
        """
        super()._start_socket()

        # wait for some socket responses
        while not len(self._depth_message_buffer):
            time.sleep(1)

    def _get_conn_key(self):
        return self._bm.start_depth_socket(self._symbol, self._depth_event, interval=self._ws_interval)

    def _process_depth_message(self, msg, buffer=False):
        """Process a depth event message.

        :param msg: Depth event message.
        :return:

        """

        if self._last_update_id is None:
            # Initial depth snapshot fetch not yet performed, buffer messages
            self._depth_message_buffer.append(msg)
            return

        if buffer and msg['u'] <= self._last_update_id:
            # ignore any updates before the initial update id
            return
        elif msg['U'] != self._last_update_id + 1:
            # if not buffered check we get sequential updates
            # otherwise init cache again
            self._init_cache()

        # add any bid or ask values
        for bid in msg['b']:
            self._depth_cache.add_bid(bid)
        for ask in msg['a']:
            self._depth_cache.add_ask(ask)

        # keeping update time
        self._depth_cache.update_time = msg['E']

        # call the callback with the updated depth cache
        if self._callback:
            self._callback(self._depth_cache)

        self._last_update_id = msg['u']

        # after processing event see if we need to refresh the depth cache
        if self._refresh_interval and int(time.time()) > self._refresh_time:
            self._init_cache()


class OptionsDepthCacheManager(BaseDepthCacheManager):

    def _get_conn_key(self):
        return self._bm.start_options_depth_socket(self._symbol, self._depth_event)
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     win = Window()
#     win.show()
#     sys.exit(app.exec_()) 
    

def start():
    """ start of GUI for module launch"""
    app = QApplication(sys.argv)
    
    screen = app.primaryScreen()
    print('Screen: %s' % screen.name())
    size = screen.size()
    print('Size: %d x %d' % (size.width(), size.height()))
    rect = screen.availableGeometry()
    print('Available: %d x %d' % (rect.width(), rect.height()))
    
    # win = Window(rect.width()//3, rect.height()//2)
    win = Window()
    win.show()
    sys.exit(app.exec_()) 

if __name__ == "__main__":
    start()