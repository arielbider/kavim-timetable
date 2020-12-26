from lxml import html
import datetime
import requests
import easygui as eg
import csv


def download(date):
    i = 18
    report = []
    if date == "":
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        date = tomorrow.strftime("%d/%m/%Y")

    for i in range(258):
        url = f"http://www.kavim-t.co.il/schedule/lineTimes.aspx?lineinfo={i}_m_4_0&monthDay={date}"
        page = requests.get(url)
        webpage = html.fromstring(page.content)

        bus_to_from = list(map(str, webpage.xpath("//div[contains(@class, 'title_from-to_txt ramle_lod_fnt')]/text()")))
        if not bus_to_from[0] == "\r\n                    ":
            bus_number = list(map(str, webpage.xpath("//div[contains(@class, 'title_line_number "
                                                     "ramle_lod_topBorder')]/text()")))[0].replace("\r\n", "").replace(
                "  ", "")
            bus_to_timetable = list(map(str, webpage.xpath(
                "//div[contains(@class, 'lineinfo_group_1')]//a[contains(@class, 'times_clock_link')]/text()")))
            bus_from_timetable = list(map(str, webpage.xpath(
                "//div[contains(@class, 'lineinfo_group_2')]//a[contains(@class, 'times_clock_link')]/text()")))

            bus_to_from[0] = bus_to_from[0].replace("\r\n", "").replace("  ", "")
            bus_to_from[1] = bus_to_from[1].replace("\r\n", "").replace("  ", "")

            for x in range(len(bus_to_timetable)):
                bus_to_timetable[x] = bus_to_timetable[x].replace("\r\n", "").replace("  ", "")

            for x in range(len(bus_from_timetable)):
                bus_from_timetable[x] = bus_from_timetable[x].replace("\r\n", "").replace("  ", "")

            if len(bus_from_timetable) < 1:
                print(f"{bus_number}, {bus_to_from[0]}, {bus_to_from[1]}, הקו אינו פעיל")
                report.append([bus_number, bus_to_from[0], bus_to_from[1], "הקו אינו פעיל"])
            else:
                print(f"{bus_number}, {bus_to_from[0]}, {bus_to_from[1]}, {','.join(bus_to_timetable)}")
                bus_csv_line = [bus_number, bus_to_from[0], bus_to_from[1]]
                for time in bus_to_timetable:
                    bus_csv_line.append(time)
                report.append(bus_csv_line)

                print(f"{bus_number}, {bus_to_from[1]}, {bus_to_from[0]}, {','.join(bus_from_timetable)}")

                bus_csv_line = [bus_number, bus_to_from[1], bus_to_from[0]]
                for time in bus_from_timetable:
                    bus_csv_line.append(time)
                report.append(bus_csv_line)

    report_name = date.replace("/", "-")
    report_file = eg.filesavebox(default=f"{report_name}.csv", filetypes=["*.csv"])
    with open(report_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(report)


if __name__ == "__main__":
    answer = input("Enter a date to run the timetable on\nFormat is DD/MM/YYYY\n")
    download(answer)
