import nest_asyncio
nest_asyncio.apply()

import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yfinance as yf

# Loglama ayarları (opsiyonel, hata ve bilgi mesajları için)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

def get_stock_price(symbol: str):
    """
    Verilen hisse sembolü için Yahoo Finance üzerinden güncel kapanış fiyatını getirir.
    BIST hisseleri için sembolün sonuna ".IS" eklenir.
    """
    yahoo_ticker = symbol.upper() + ".IS"
    stock = yf.Ticker(yahoo_ticker)
    # Günlük veriyi çekiyoruz
    data = stock.history(period="1d")
    if not data.empty:
        price = data["Close"].iloc[-1]
        return price
    else:
        return None

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /price komutu ile gönderilen hisse sembolü için fiyatı getirir.
    Örnek kullanım: /price THYAO
    """
    if context.args:
        symbol = context.args[0].upper()
        price_value = get_stock_price(symbol)
        if price_value is not None:
            await update.message.reply_text(f"{symbol} fiyatı: {price_value:.2f} TL")
        else:
            await update.message.reply_text("Fiyat bilgisi alınamadı. Sembolü kontrol edin.")
    else:
        await update.message.reply_text("Lütfen hisse senedi sembolü girin. Örnek: /price THYAO")

async def main() -> None:
    TOKEN = "7890256860:AAEM6-fp-JtFv7_pdzo6Fi-IPjXF8sUuIiU"  # BotFather'dan aldığın token
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("price", price))

    # Botu polling ile çalıştırıyoruz (Telegram'dan gelen mesajları sürekli dinler)
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
