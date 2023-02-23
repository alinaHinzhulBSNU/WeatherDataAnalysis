import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

# КОНСТАНТИ
FILE_PATH = "weather_data.csv"
COLS = ["Timestamp", "Temperature 1", "Temperature 2", "Humidity"]
TYPES = {"Temperature 1": float, "Temperature 2": float, "Humidity": float}

# ДІАПАЗОН ДАТ
START_DATE = pd.Timestamp(2023, 1, 1, 0, 0, 0)
END_DATE = pd.Timestamp(2023, 2, 21, 23, 59, 59)
DAY_OFFSET = 5


# ЧИТАННЯ ДАНИХ З ФАЙЛУ
def read_weather_data_from_csv(path, col_names):
    return pd.read_csv(filepath_or_buffer=path,
                       sep=";",
                       decimal=",",
                       parse_dates=["Timestamp"],
                       date_parser=lambda x: pd.to_datetime(x, dayfirst=True),
                       low_memory=True,
                       usecols=col_names,
                       dtype=TYPES)


# ОБРОБКА ПРОЧИТАНИХ ДАНИХ
def process_weather_data(data_frame, start_date, end_date, day_offset):
    # Середні значення температури та вологості в обрані дні
    averages = pd.DataFrame()

    date = start_date
    while date < end_date:
        # Всі результати вимірювань за певний день
        all_day_measurements = data_frame.loc[data_frame["Timestamp"].dt.date == date.date()]

        # Розрахунок середніх значень для певної дати
        averages = pd.concat([averages, pd.DataFrame.from_records(
            [{"Timestamp": date.date(),
              "Humidity": all_day_measurements["Humidity"].mean(),
              "Temperature 1": all_day_measurements["Temperature 1"].mean(),
              "Temperature 2": all_day_measurements["Temperature 2"].mean()}]
        )])

        # Розрахунок наступної дати з певним кроком
        date = date + pd.DateOffset(days=day_offset)

    return averages


# ФОРМАТОВАНЕ ВИВЕДЕННЯ РЕЗУЛЬТАТІВ РОЗРАХУНКІВ
def print_data(data):
    headers = ["Дата (YYYY-MM-DD)", "Вологість (%)", "Температура 1 (°C)", "Температура 2 (°C)"]
    table = tabulate(data, headers=headers, tablefmt='psql', showindex=False)
    print(table)


# ГРАФІК ЗМІНИ ВОЛОГОСТІ
def plot_humidity(data):
    plt.plot(data["Timestamp"], data["Humidity"], color="purple", label="Humidity")
    plt.xticks(ticks=data["Timestamp"], labels=data["Timestamp"])

    plt.title("Графік зміни вологості")
    plt.xlabel("Дата (YYYY-MM-DD)")
    plt.ylabel("Вологість (%)")

    plt.legend()
    plt.show()


# ГРАФІК ЗМІНИ ТЕМПЕРАТУРИ
def plot_temperature(data):
    plt.plot(data["Timestamp"], data["Temperature 1"], color="red", label="Temperature 1")
    plt.plot(data["Timestamp"], data["Temperature 2"], color="blue", label="Temperature 2")
    plt.xticks(ticks=data["Timestamp"], labels=data["Timestamp"])

    plt.title("Графік зміни температури")
    plt.xlabel("Дата (YYYY-MM-DD)")
    plt.ylabel("Температура (°C)")

    plt.legend()
    plt.show()


if __name__ == "__main__":
    # Розрахунки
    df = read_weather_data_from_csv(FILE_PATH, COLS)
    result = process_weather_data(df, START_DATE, END_DATE, DAY_OFFSET)

    # Виведення результату розрахунків
    print_data(result)

    # Побудова графіків
    plot_humidity(result)
    plot_temperature(result)
