#include "window.h"

#include <QApplication>
#include <QPushButton>

Window::Window(QWidget *parent) :
    QWidget(parent) {
    int windowX = 600;
    int windowY = 400;
    setFixedSize(windowX, windowY);

    int width_buttons = 160;
    int height_buttons = 30;

    int portPermissionX = 10;
    int portPermissionY = 10;
    portPermission = new QPushButton("Dar permissão", this);
    portPermission->setGeometry(portPermissionX, portPermissionX, width_buttons, height_buttons);
    portPermission->setCheckable(true);
    connect(portPermission, SIGNAL (clicked(bool)), this, SLOT(slotPermissionButtonClicked(bool)));

    int startReadingX = portPermissionX;
    int startReadingY = portPermissionY + 40;
    startReading = new QPushButton("Iniciar leituras", this);
    startReading->setGeometry(startReadingX, startReadingY, width_buttons, height_buttons);
    startReading->setCheckable(true);
    connect(startReading, SIGNAL (clicked(bool)), this, SLOT(slotStartButtonClicked(bool)));

    int quitButtonX = windowX - width_buttons - 20;
    int quitButtonY = windowY - height_buttons - 20;
    quitButton = new QPushButton("Sair", this);
    quitButton->setGeometry(quitButtonX, quitButtonY, width_buttons, height_buttons);
    connect(quitButton, SIGNAL (clicked()), QApplication::instance(), SLOT (quit()));
}

void Window::slotPermissionButtonClicked(bool checked) {
    if (checked) {
        portPermission->setText("Checked");
    } else {
        portPermission->setText("Dar permissão");
    }
}

void Window::slotStartButtonClicked(bool checked) {
    if (checked) {
        startReading->setText("Checked");
    } else {
        startReading->setText("Iniciar leituras");
    }
}
