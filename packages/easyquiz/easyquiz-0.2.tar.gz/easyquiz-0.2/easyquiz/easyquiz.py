""" Module to create quick quizzes for IPython

Raises:
    KeyError: If language selected is not defined

    TypeError: If trying to change the title of a Quiz instance object with a
    type different from str

    TypeError: If trying to change the description of a Quiz instance object
    with a type different from str
"""

import ipywidgets as widgets
from ipywidgets import Layout
from IPython.display import clear_output
import random
import json
import os


class QuizQuestion():
    """ Class to define questions for easyquiz.Question
    """

    def __init__(self, statement=None, options=None, solution=None):
        """ Initializes QuizQuestion object. If parameter values are not
        specified or are not valid defaul to None.

        Args:
            statement (str, optional): Question's statement. Defaults to None.

            options (list of str, optional): Possible answers to show.
            Defaults to None.

            solution (str, optional): Correct solution to answer.
            Defaults to None.
        """

        self.question_type = 'multiple_choice'
        self.add_statement(statement)
        self.add_options(options)
        self.add_solution(solution)

    def __str__(self):
        return 'easyQuiz Question (Statement: {}, Options: {}, Solution: {}'.\
            format(self.statement_status, self.options_status,
                   self.solution_status)

    def __repr__(self):
        return 'easyQuiz.QuizQuestion (Sta:{},Opt:{},Sol:{})'.format(
            self.statement_status, self.options_status, self.solution_status)

    def add_statement(self, statement):
        """ Adds statement. If an invalid type is provided, the statement value
        is set to None

        Args:
            statement (str): Question statement
        """
        if self.check_statement(statement):
            self._statement = statement
            self.statement_status = 'OK'
        else:
            self._statement = None
            self.statement_status = 'X'

    def check_statement(self, statement):
        """ Checks if paramenter is valid

        Args:
            statement (str): Statement to be checked

        Returns:
            [bool]: True if statement is valid, False otherwise
        """
        return isinstance(statement, str)

    def add_options(self, options):
        """ Adds possible answers. If an invalid type is provided, the options
        value is set to None

        Args:
            options (list of str): Possible answers
        """
        if options and self.check_options(options):
            self._options = options
            self._alternatives = widgets.RadioButtons(options=options,
                                description='',
                                disabled=False,
                                layout=widgets.Layout(width='100%'))

            self.options_status = 'OK'
        else:
            self._options = None
            self._alternatives = None
            self.options_status = 'X'

    def check_options(self, options):
        """ Checks if options is valid

        Args:
            options (list of str): Options candidate

        Returns:
            [bool]: True if valid, False otherwise
        """
        return not any(not isinstance(element, str) for element in options)

    def add_solution(self, solution):
        """ Adds solution. If an invalid type is provided, the options value is
        set to None

        Args:
            solution (str): Correct answer to the question
        """
        if self.check_solution(solution):
            self._solution = solution
            self.solution_status = 'OK'
        else:
            self._solution = None
            self.solution_status = 'X'

    def check_solution(self, solution):
        """ Checks if options is valid

        Args:
            solution (str): Solution candidate

        Returns:
            [bool]: True if valid, False otherwise
        """
        return isinstance(solution, str)

    def correct(self):
        """ Contrast answer with solution

        Returns:
            [bool]: True if correct, False otherwise
        """
        return self._solution == self._alternatives.value

    def get_dict(self):
        """ Return all data stored in a dict

        Returns:
            [dict]: Object parameters for import
        """
        output_dict = {'question_type': self.question_type,
                       'statement': self._statement,
                       'options': self._options,
                       'solution': self._solution}

        return output_dict


class Quiz():
    """ Class to define a Quiz for easyquiz
    """

    def __init__(self, title=None, description=None,  lang='eng',
                 load_json=False):
        """ Initializes Quiz object. If parameter values are not specified or
        are not valid defaul to None.

        Args:
            title (str, optional): Quiz title to show. If set to None, title
            and description are not shown. Defaults to None.

            description (str, optional): Description of the quiz to be shown
            after the title. If title is set no none, description is not shown
            either. Defaults to None.

            lang (str, optional): Quiz language. Defaults to 'eng.

            load_json (str or bool, optional): Path to create the object with a
            json file. If a file is provided the rest of the parameters are
            ignored. Defaults to False.

        Raises:
            KeyError: If language is not valid
        """

        if load_json:
            with open(load_json, 'r') as f:
                quiz_data = json.load(f)

            self.language = quiz_data['language']
            self.title = quiz_data['title']
            self.description = quiz_data['description']
            self.questions = []
            for question in quiz_data['questions']:
                self.questions.append(QuizQuestion(
                                       statement=question['statement'],
                                       options=question['options'],
                                       solution=question['solution']))
        else:
            self.language = lang
            self.title = title
            self.description = description
            self.questions = []

        this_dir, this_filename = os.path.split(__file__)
        LANGS_PATH = os.path.join(this_dir, "langs.json")
        
        try:
            with open(LANGS_PATH, 'r') as f:
                languages = json.load(f)
        except FileNotFoundError:
            print('Language file not found, defaults loaded.')
            languages = {'eng': {'button_text': 'Check',
                                 'correct_msg': 'Well done! Correct answer.',
                                 'wrong_msg': 'Ooops, looks like something went wrong. Think it again!',
                                'intro': 'Question'},
                         'esp': {'button_text': 'Comprobar',
                                 'correct_msg': '¡Respuesta correcta!',
                                 'wrong_msg': 'Ooops, parece que no lo has entendido bien. ¡Vuelve a intentarlo!',
                                 'intro': 'Pregunta'}}

        try:
            button_text = languages[self.language]['button_text']
            self.correct_msg = languages[self.language]['correct_msg']
            self.wrong_msg = languages[self.language]['wrong_msg']
            self.intro = languages[self.language]['intro']
        except KeyError:
            raise KeyError('Language "{}" not supported'.format(self.language))

        b_margin = '20px 0px 20px 0px'
        self.check = widgets.Button(description=button_text,
                                    layout=Layout(margin=b_margin))
        self.out = widgets.Output()
        self.check.on_click(self.check_responses)

    def __str__(self):
        return 'easyquiz Quiz ({} questions)'.format(len(self.questions))

    def __repr__(self):
        return 'easyquiz.Quiz({})'.format(len(self.questions))

    def add_questions(self, questions):
        """ Adds a question to the Quiz

        Args:
            questions (easyquiz.QuizQueston): easyquiz Question objec
        """
        for question in questions:
            self.questions.append(question)

    def show(self, rand=False):
        """ Shows the quiz

        Args:
            rand (bool, optional): Show the questions in randomly sorted.
            Defaults to False.
        """
        if self.title:
            print('\n\033[1m', '{}'.format(self.title), '\033[0m')
            if self.description:
                print('\n{}'.format(self.description))

        questions_show = self.questions.copy()
        if rand:
            random.shuffle(questions_show)

        for i, question in enumerate(questions_show):
            print('\n\033[1m', '{}: {}'.format(i+1, question._statement),
                  '\033[0m')
            display(question._alternatives)

        display(self.check)
        display(self.out)

    def check_responses(self, button):
        """ Function exectuded when pression 'Check' button. Corrects the quiz
        and shows feedback

        Args:
            button (ipywidgets.Button): Quiz button
        """
        with self.out:
            clear_output()

        for i, question in enumerate(self.questions):
            self.create_feedback(i+1, question.correct())

    def create_feedback(self, question_no, correct=False):
        """ Creates the feedback for a question and adds is in the output space

        Args:
            question_no (int): Number of the question to be displayed in the
            feedback statement.

            correct (bool, optional): Correctness of the answer.
            Defaults to False.
        """
        bcolors = {'start': '\033[95m',
                   'green': '\033[32m',
                   'red': '\033[31m',
                   'magenta': '\033[35m',
                   'end': '\033[0m'}

        msg = '{} {}: {}'.format(self.intro, question_no, bcolors['start'])

        if correct:
            msg += '{}{}'.format(bcolors['green'], self.correct_msg)
        else:
            msg += '{}{}'.format(bcolors['red'], self.wrong_msg)

        msg += bcolors['end']

        with self.out:
            print(msg)

    def change_title(self, title):
        """ Changes quiz title to display.

        Args:
            title (str): Quiz title.

        Raises:
            TypeError: title type different to str
        """
        if isinstance(title, str):
            self.title = title
        elif title is None:
            self.title = None
        else:
            raise TypeError('str expect, not {}'.format(type(title)))

    def change_description(self, description):
        """ Changes quiz description to display.

        Args:
            description (str): Quiz description

        Raises:
            TypeError: description different to str
        """
        if type(description) == str:
            self.description = description
        elif description is None:
            self.description = None
        else:
            raise TypeError('str expect, not {}'.format(type(description)))

    def save_json(self, path='quiz.json'):
        """ Saves instance attributes to a json file

        Args:
            path (str, optional): Path of save file. Defaults to 'quiz.json'.
        """

        questions = []
        for question in self.questions:
            questions.append(question.get_dict())

        output_dict = {'title': self.title,
                       'description': self.description,
                       'language': self.language,
                       'questions': questions}

        with open(path, "w") as f:
            json.dump(output_dict, f, indent=4)
