import gradio as gr
from accounts import Account, get_share_price

account = Account(1000)

def deposit(amount):
    try:
        account.deposit(float(amount))
        return str(account)
    except ValueError as e:
        return f"Error: {e}"

def withdraw(amount):
    try:
        account.withdraw(float(amount))
        return str(account)
    except ValueError as e:
        return f"Error: {e}"

def buy(symbol, quantity, price):
    try:
        account.buy(symbol, int(quantity), float(price))
        return str(account)
    except ValueError as e:
        return f"Error: {e}"

def sell(symbol, quantity, price):
    try:
        account.sell(symbol, int(quantity), float(price))
        return str(account)
    except ValueError as e:
        return f"Error: {e}"

def get_portfolio_value():
    return f"Portfolio Value: ${account.get_portfolio_value():.2f}"

def get_profit_loss():
    return f"Profit/Loss: ${account.get_profit_loss():.2f}"

def get_holdings():
    return f"Holdings: {account.get_holdings()}"

def get_transactions():
    return f"Transactions: {account.get_transactions()}"


with gr.Blocks() as demo:
    gr.Markdown("# Simple Trading Simulation")

    with gr.Tab("Deposit"):
        amount = gr.Number(label="Amount")
        deposit_button = gr.Button("Deposit")
        deposit_output = gr.Textbox(label="Output")
        deposit_button.click(fn=deposit, inputs=amount, outputs=deposit_output)

    with gr.Tab("Withdraw"):
        amount = gr.Number(label="Amount")
        withdraw_button = gr.Button("Withdraw")
        withdraw_output = gr.Textbox(label="Output")
        withdraw_button.click(fn=withdraw, inputs=amount, outputs=withdraw_output)

    with gr.Tab("Buy"):
        symbol = gr.Textbox(label="Symbol")
        quantity = gr.Number(label="Quantity")
        price = gr.Number(label="Price")
        buy_button = gr.Button("Buy")
        buy_output = gr.Textbox(label="Output")
        buy_button.click(fn=buy, inputs=[symbol, quantity, price], outputs=buy_output)

    with gr.Tab("Sell"):
        symbol = gr.Textbox(label="Symbol")
        quantity = gr.Number(label="Quantity")
        price = gr.Number(label="Price")
        sell_button = gr.Button("Sell")
        sell_output = gr.Textbox(label="Output")
        sell_button.click(fn=sell, inputs=[symbol, quantity, price], outputs=sell_output)

    with gr.Tab("Portfolio"):
        portfolio_value = gr.Textbox(label="Portfolio Value")
        profit_loss = gr.Textbox(label="Profit/Loss")
        holdings = gr.Textbox(label="Holdings")
        transactions = gr.Textbox(label="Transactions")
        gr.Button("Update").click(fn=[get_portfolio_value, get_profit_loss, get_holdings, get_transactions], outputs=[portfolio_value, profit_loss, holdings, transactions])

demo.launch()