import sys
from PyQt5.QtWidgets import QApplication
from controller import RegexController
from view import RegexView
from model import RegexModel


def main():
    app = QApplication(sys.argv)

    # Create MVC components
    model = RegexModel()
    view = RegexView()
    controller = RegexController(model, view)

    # Initialize the application
    controller.initialize()

    # Show the view and start application
    view.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()