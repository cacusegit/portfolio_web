from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import plotly.graph_objs as go

today_ = datetime.today().strftime('%Y-%m-%d')
sort = datetime.today().year


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless=new")
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(chrome_options)
driver.get(f'https://github.com/cacusegit?tab=overview&from=2025-01-01&to={today_}')
driver.implicitly_wait(10)


def get_contribution_count():
    contributions = driver.find_element(By.XPATH,
                                        value='//*[@id="user-profile-frame"]/div/div[2]/div/div[1]/div[1]/div[1]/h2')
    return contributions.text


def get_commit_data():
    tooltip_texts = []
    commits = driver.find_elements(By.CSS_SELECTOR, 'tool-tip[for^="contribution-day"]')

    for tooltip in commits:
        tooltip_text = tooltip.text.strip()
        tooltip_texts.append(tooltip_text)

    return tooltip_texts


def handle_contributions(scraped_data):
    contributions = []
    for each in scraped_data:
        new_list = each.split(" ")
        if new_list[0] == "No":
            contributions.append(0)
        else:
            contributions.append(new_list[0])
    int_values = [int(value) for value in contributions]
    return int_values


def handle_dates(scraped_data):
    dates = []
    for each in scraped_data:
        new_list = each.split(" ")
        date = new_list[3] + " " + new_list[4].strip(".").strip('th').strip("rd").strip('s').strip('n')
        dates.append(date)
    return dates


def create_df(scraped_data):
    contributions = handle_contributions(scraped_data)
    dates = handle_dates(scraped_data)

    filtered_dates = [date for date, contrib in zip(dates, contributions) if contrib != 0]
    filtered_contributions = [contrib for contrib in contributions if contrib != 0]

    df = pd.DataFrame({
        'Date': filtered_dates,
        'Contributions': filtered_contributions
    })
    df.to_csv('data.csv', index=False)


def create_graph(data_file):
    df = pd.read_csv(data_file)

    df["Date"] = pd.to_datetime(df['Date'] + " " + str(sort), format='%B %d %Y')
    df = df.sort_values(by="Date")

    fig = go.Figure(data=[go.Bar(
        x=df['Date'],
        y=df['Contributions'],
        marker_color='#a478ae'
    )])

    fig.update_layout(
        title='GitHub Contributions',
        xaxis_title='Date',
        yaxis_title='Contributions',
        paper_bgcolor="#090a0f",
        font_color="#dfe0ec",
        plot_bgcolor="rgb(20,20,26)",
        hoverlabel=dict(font_color='#dfe0ec')
    )

    return fig.to_html(full_html=False)
