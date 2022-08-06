import datetime
mydates = [
    {
        "title": "Call microwave service from IFB",
        "datetime": "30-Jun-2022:00:00",
        "dateandtime": "Thursday, 30 June 2022, 12:00 AM"
    },
    {
        "title": "Brush Teeth",
        "datetime": "30-Jul-2022:00:00",
        "dateandtime": "Saturday, 30 July 2022, 12:00 AM"
    },
    {
        "title": "Megha birthday",
        "datetime": "03-Dec-2022:00:00",
        "dateandtime": "Saturday, 3 December 2022, 12:00 AM"
    },
    {
        "title": "Aishwarya Birthday",
        "datetime": "05-Jan-2023:00:00",
        "dateandtime": "Thursday, 5 January 2023, 12:00 AM"
    },
    {
        "title": "Suravi Birthday",
        "datetime": "19-Oct-2022:00:00",
        "dateandtime": "Wednesday, 19 October 2022, 12:00 AM"
    },
    {
        "title": "Pavan Kumar jss birthday",
        "datetime": "18-Nov-2022:00:00",
        "dateandtime": "Friday, 18 November 2022, 12:00 AM"
    },
    {
        "title": "Yamini birthday",
        "datetime": "24-Nov-2022:00:00",
        "dateandtime": "Thursday, 24 November 2022, 12:00 AM"
    },
    {
        "title": "Car emission test renewal. Ends on 12th Nov",
        "datetime": "06-Nov-2022:00:00",
        "dateandtime": "Sunday, 6 November 2022, 12:00 AM"
    },
    {
        "title": "Sourabh intel bday",
        "datetime": "11-Dec-2022:00:00",
        "dateandtime": "Sunday, 11 December 2022, 12:00 AM"
    },
    {
        "title": "Nisarga Birthday",
        "datetime": "12-Dec-2022:00:00",
        "dateandtime": "Monday, 12 December 2022, 12:00 AM"
    },
    {
        "title": "Vishwas Birthday",
        "datetime": "28-Oct-2022:00:00",
        "dateandtime": "Friday, 28 October 2022, 12:00 AM"
    },
    {
        "title": "Shravan birthday",
        "datetime": "10-Oct-2022:00:00",
        "dateandtime": "Monday, 10 October 2022, 12:00 AM"
    },
    {
        "title": "Kailash Birthday",
        "datetime": "18-Aug-2022:00:00",
        "dateandtime": "Thursday, 18 August 2022, 12:00 AM"
    },
    {
        "title": "Shashank birthday",
        "datetime": "02-Oct-2022:00:00",
        "dateandtime": "Sunday, 2 October 2022, 12:00 AM"
    },
    {
        "title": "SANJEEV BHAVA BIRTHDAY",
        "datetime": "29-Sep-2022:00:00",
        "dateandtime": "Thursday, 29 September 2022, 12:00 AM"
    },
    {
        "title": "Sushmita Birthday",
        "datetime": "22-Aug-2022:00:00",
        "dateandtime": "Monday, 22 August 2022, 12:00 AM"
    },
    {
        "title": "Pratheek birthday",
        "datetime": "21-Sep-2022:00:00",
        "dateandtime": "Wednesday, 21 September 2022, 12:00 AM"
    },
    {
        "title": "Anuarpith birthday",
        "datetime": "12-Sep-2022:00:00",
        "dateandtime": "Monday, 12 September 2022, 12:00 AM"
    },
    {
        "title": "Shachi akka birthday",
        "datetime": "11-Aug-2022:00:00",
        "dateandtime": "Thursday, 11 August 2022, 12:00 AM"
    }
]

print(mydates.sort(key=lambda x:x['datetime']))