import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import datetime


class Librus:
    def __init__(self):
        """
         Initializes a new instance of the Librus class.
        """

        self.session = None

    def login(self, username, password):
        """
            Logs in to the Librus API.
            :param username: The username of the Librus account
            :param password: The password of the Librus account.
        """

        self.session = requests.Session()

        auth_url = 'https://api.librus.pl/OAuth/Authorization?client_id=46&response_type=code&scope=mydata'
        self.session.get(url=auth_url)

        login_url = 'https://api.librus.pl/OAuth/Authorization?client_id=46'
        response = self.session.post(url=login_url, data={'action': 'login', 'login': username, 'pass': password})

        json_response = response.json()

        if not json_response.get('status') == 'ok' or not json_response.get('goTo'):
            raise RuntimeError("Login Failed")

        redirect_url = urljoin(response.url, json_response['goTo'])
        self.session.get(url=redirect_url)

    def get_student_info(self):
        """
        Get student's information including fullname, classname, classindex, educator, login.
        :return: A tuple containing the student's fullname, classname, classindex, educator, login.
        :rtype: tuple
        :return: fullname, classname, classindex, educator, login
        """

        # Make GET request to the URL
        url = 'https://synergia.librus.pl/informacja'
        response = self.session.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            raise RuntimeError("Nie udało się pobrać informacji o uczniu")

        # Parse the response with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all table rows with class line0 or line1
        rows = soup.find_all('tr', class_=lambda x: x in ['line0', 'line1'])

        # Initialize an empty dictionary to store the results
        result_dict = {}

        # Loop through each row
        for row in rows:
            # Find the th and td elements in each row
            th_element = row.find('th', class_='big')
            td_element = row.find('td')

            # Extract text from th and td elements
            if th_element and td_element:
                th_text = th_element.get_text(strip=True)
                td_text = td_element.get_text(strip=True)

                # Add th_text as key and td_text as value to the result dictionary
                result_dict[th_text] = td_text

        fullname = result_dict.get('Imię i nazwisko ucznia')
        classname = result_dict.get('Klasa')[:3]

        #make classname with no spaces between letters
        classname = classname.replace(" ", "")

        #make classname to uppercase
        classname = classname.upper()

        classindex = result_dict.get('Nr w dzienniku')
        educator = result_dict.get('Wychowawca')
        login = result_dict.get('Login')

        return fullname, classname, classindex, educator, login


    def get_student_grades(self):
        """
        Get all grades for the student.
        :return: A list of tuples containing the grade, comment, title, added_date, teacher, correction_grade, added_by.
        :rtype: list
        :return: grades
        """
        # Make GET request to the URL
        url = 'https://synergia.librus.pl/przegladaj_oceny/uczen'
        response = self.session.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            raise RuntimeError("Nie udało się pobrać ocen")

        # Parse the response with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the container holding student's grades
        container = soup.find_all('table', class_='decorated stretch')

        # Extract the grades from the container
        grades = []
        for table in container:
            for grade_row in table.find_all('tr', class_='detail-grades'):
                grade_data = grade_row.find_all('td')
                grade = grade_data[0].text
                comment = grade_data[1].text
                title = grade_data[2].text
                added_date = grade_data[3].text
                teacher = grade_data[4].text
                correction_grade = grade_data[5].text
                added_by = grade_data[6].text
                grades.append((grade, comment, title, added_date, teacher,correction_grade, added_by))

        return grades

    def get_teachers(self):
        """
        Get all teachers that gave the student a grade.
        :return: A list of teacher names.
        :rtype: list
        :return: teachers
        """

        data = self.get_student_grades()
        teachers = []
        for teacher in data:
            teachers.append(teacher[4])

        teachers = set(teachers)

        #Remove empy elements from teachers
        teachers = list(filter(None, teachers))

        return teachers

    def get_grades(self):
        """
        Get all grades for each subject.
        :return: A dictionary with subject names as keys and grades as values.
        :rtype: dict
        :return: grades
        """

        # Make GET request to the URL
        url = 'https://synergia.librus.pl/przegladaj_oceny/uczen'
        response = self.session.get(url)

        if response.status_code != 200:
            raise RuntimeError("Nie udało się pobrać ocen")

        soup = BeautifulSoup(response.text, "html.parser")

        grades = {}
        # Loop through each row that contains grades, assumed to be similarly structured to subjects
        for subject_row in soup.find_all(class_="line0") + soup.find_all(class_="line1"):
            if len(subject_row.find_all("td")) > 10 and subject_row.find_all("td")[1].text != "Ocena":
                subject_name = subject_row.find_all("td")[1].text.strip()
                if "\n" not in subject_name:  # Filtering out new lines if present in the name
                    # Assuming grades are in the subsequent td elements or structured similarly
                    subject_grades = [td.text.strip() for td in subject_row.find_all("td")[2:]]
                    grades[subject_name] = subject_grades

        return grades


    def get_final_grades(self):
        """
        Get the final grades for each subject.
        :return: A dictionary with subject names as keys and final grades as values.
        :rtype: dict
        :return: final_grades
        """
        grades = self.get_grades()
        final_grades = {}
        for key in grades:
            final_grades[key] = grades[key][-1]

        return final_grades

    def get_subjects(self):
        """
        Get all subjects the student has.
        :return: A list of subject names.
        :rtype: list
        :return: subjects
        """

        subjects = self.get_grades()
        subjects = list(subjects.keys())

        return subjects

    def get_grades_for_specific_subject(self, subject_name):
        """
        Get all grades for a specific subject.
        :param subject_name: The name of the subject.
        :type subject_name: str
        :return: A dictionary with grade types as keys and grades as values.
        :rtype: dict
        :param subject_name:
        :return: grades_dict
        """

        grades = self.get_grades()

        subject_grades = grades.get(subject_name)

        for grade in subject_grades:
            if grade == '':
                subject_grades.remove(grade)

        grades_dict = {
            "Oceny Z Pierwszego Semestru": subject_grades[0],
            "Średnia Z Pierwszego Semestru": subject_grades[1],
            "Przewidywana Ocena Z Pierwszego Semestru": subject_grades[2],
            "Ocena Końcowa Z Pierwszego Semestru": subject_grades[3],
            "Oceny Z Drugiego Semestru": subject_grades[4],
            "Średnia Z Drugiego Semestru": subject_grades[5],
            "Przewidywana Ocena Z Drugiego Semestru": subject_grades[6],
            "Ocena Końcowa Z Drugiego Semestru": subject_grades[7],
        }

        for key in grades_dict:
            grades_dict[key] = grades_dict[key].replace("\n", ",")

        return grades_dict

    def get_events(self):
        """
        Get all events from the calendar for this month.
        :return: A list of dictionaries with event dates as keys and event descriptions as values.
        :rtype: list
        :return: events
        """
        url = "https://synergia.librus.pl/terminarz"

        response = self.session.get(url)

        if response.status_code != 200:
            raise RuntimeError("Nie udało się pobrać terminarza")

        soup = BeautifulSoup(response.text, "html.parser")

        month = datetime.datetime.now().month

        months = ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"]



        events = [months[month-1]]

        # Find all div elements with the class 'centrowanie'
        centrowanie_divs = soup.find_all("div", class_="centrowanie")
        for div in centrowanie_divs:
            event_details = {}

            # Assuming each event is within a 'div' with class 'kalendarz-dzien'
            for event_div in div.find_all("div", class_="kalendarz-dzien"):
                day_number = event_div.find("div", class_="kalendarz-numer-dnia").text.strip() if event_div.find("div",
                                                                                                                 class_="kalendarz-numer-dnia") else None
                descriptions = []
                event_tables = event_div.find_all("table")

                for table in event_tables:
                    for row in table.find_all("tr"):
                        cell = row.find("td")
                        if cell:
                            descriptions.append(cell.get_text(strip=True))

                event_details[day_number] = descriptions

            if event_details:
                events.append(event_details)

        return events

    def get_today_events(self):
        """
        Get all events for today.
        :return: A dictionary with event dates as keys and event descriptions as values.
        :rtype: dict
        :return: events
        """
        events = self.get_events()
        today = datetime.datetime.now().day

        # get the event with the key today
        today_events = events[1].get(str(today))

        return today_events

    def is_there_a_test_today(self):
        """
        Check if there is a sprawdzian today
        :return: True if there is a test today, False otherwise.
        :rtype: bool
        :return: test_today
        """
        today_events = self.get_today_events()
        test_today = False
        for event in today_events:
            if "Sprawdzian" in event:
                test_today = True
                break

        return test_today


