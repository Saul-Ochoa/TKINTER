import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk
import yfinance  as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import mplfinance as mpf

# funcion para obtener los datos de las acciones
def get_stock_data(stock_symbol,period='1mo'):
    stock_data=yf.download(stock_symbol,period=period)
    return stock_data

def plot_stock_data(stock_data):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))  # 2 filas, 2 columnas

    # Gráfico 1: Precio de Cierre
    ax1 = axes[0, 0]
    ax1.plot(stock_data.index, stock_data['Close'], label='Close Price', color='#00FF00')
    ax1.set_title('Google Stock Price', color='#00FF00', fontsize=14,weight='bold')
    #ax1.set_xlabel('Date', color='#00FF00')
    #ax1.set_ylabel('Close Price', color='#00FF00')
    ax1.grid(True, color='#444444')
    ax1.legend(facecolor='#00FF00', edgecolor='#00FF00', fontsize=8, loc='upper left')
    ax1.set_facecolor('#000000')
    ax1.xaxis_date()
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right', color='#0a0a0a')

    # Gráfico 2: Volumen
    ax2 = axes[0, 1]
    ax2.bar(stock_data.index, stock_data['Volume'], color='#00FF00')
    ax2.set_title('Trading Volume', color='#00FF00', fontsize=14,weight='bold')
    #ax2.set_xlabel('Date', color='#00FF00')
    #ax2.set_ylabel('Volume', color='#00FF00')
    ax2.grid(True, color='#444444')
    ax2.set_facecolor('#000000')
    ax2.xaxis_date()
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right', color='#0a0a0a')

    # Gráfico 3: Velas Japonesas
    ax3 = axes[1, 0]
    mpf.plot(stock_data, type='candle', ax=ax3, style='charles', 
             volume=False, mav=(2), datetime_format='%Y-%m-%d',
             xrotation=45, ylabel='Price', ylabel_lower='Volume')
    ax3.set_title('Candlestick Chart', color='#00FF00', fontsize=14,weight='bold')
    ax3.set_facecolor('#000000')
    ax3.set_ylabel('',color='#ffffff')
    ax3.grid(True,color='#444444')
    
    # Gráfico 4: Media Móvil
    ax4 = axes[1, 1]
    stock_data['50_MA'] = stock_data['Close'].rolling(window=2).mean()
    ax4.plot(stock_data.index, stock_data['Close'], label='Close Price', color='#00FF00')
    ax4.plot(stock_data.index, stock_data['50_MA'], label='2-Month MA', color='#FF00FF')
    ax4.set_title('50-Day Moving Average', color='#00FF00', fontsize=14,weight='bold')
    #ax4.set_xlabel('Date', color='#00FF00')
    #ax4.set_ylabel('Close Price', color='#00FF00')
    ax4.grid(True, color='#444444')
    ax4.legend(facecolor='#00FF00', edgecolor='#00FF00', fontsize=8, loc='upper left')
    ax4.set_facecolor('#000000')
    ax4.xaxis_date()
    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right', color='#0a0a0a')

    fig.tight_layout()
    return fig

def create_dashboard():
    root = tk.Tk()
    root.title('Financial Dashboard - Google Stock')
    # Obtener datos
    stock_data = get_stock_data('GOOGL')
    # Crear un marco para contener el gráfico
    frame = tk.Frame(root, bg='#877c7e')  # Fondo gris para el marco
    frame.pack(fill=tk.BOTH, expand=True)
    # Crear el gráfico
    figure = plot_stock_data(stock_data)
    # Integrar el gráfico en Tkinter
    canvas = FigureCanvasTkAgg(figure, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    root.mainloop()

if __name__ == "__main__":
    create_dashboard()
