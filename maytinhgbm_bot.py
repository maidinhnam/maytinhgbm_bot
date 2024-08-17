from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Chào mừng bạn! Gõ lệnh /calculate theo định dạng: /calculate <odds1> <odds2> [odds3] <total_amount>'
    )

async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Lấy các tham số từ câu lệnh
        args = context.args
        if len(args) < 3:
            await update.message.reply_text('Vui lòng nhập ít nhất 2 tỷ lệ cược và tổng số tiền.')
            return

        # Chuyển đổi tỷ lệ cược và số tiền tổng thành số thực
        odds = list(map(float, args[:-1]))
        total_amount = float(args[-1])

        if len(odds) < 2:
            await update.message.reply_text('Bạn cần nhập ít nhất 2 tỷ lệ cược.')
            return
        
        if len(odds) > 3:
            await update.message.reply_text('Hiện tại bot hỗ trợ tối đa 3 tỷ lệ cược.')
            return

        # Tính toán tổng tỷ lệ nghịch
        total_inverse = sum(1/o for o in odds)
        
        if total_inverse >= 1:
            await update.message.reply_text('Không có cơ hội cược chênh lệch (tổng tỷ lệ nghịch >= 1).')
            return

        # Tính số tiền cần đặt cược
        stakes = [total_amount * (1 / o / total_inverse) for o in odds]
        profits = [stake * o - total_amount for stake, o in zip(stakes, odds)]

        # Tạo kết quả trả về
        result = '\n'.join(
            f"Số tiền đặt cược vào nhà cái {i+1}: {stakes[i]:.2f} VND\nLợi nhuận nếu nhà cái {i+1} thắng: {profits[i]:.2f} VND"
            for i in range(len(odds))
        )

        await update.message.reply_text(result)

    except Exception as e:
        await update.message.reply_text(f'Có lỗi xảy ra: {str(e)}')

def main():
    TOKEN = '7370446922:AAGEmMFDFC9yHLs8i6j6dRq2mfClBDM3Xzs'
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('calculate', calculate))
    
    application.run_polling()

if __name__ == '__main__':
    main()
