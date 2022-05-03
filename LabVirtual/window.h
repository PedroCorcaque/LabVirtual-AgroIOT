#ifndef WINDOW_H
#define WINDOW_H

#include <QWidget>

class QPushButton;
class Window : public QWidget {
    Q_OBJECT
    public:
        explicit Window(QWidget *parent = 0);
    private slots:
        void slotPermissionButtonClicked(bool checked);
        void slotStartButtonClicked(bool checked);
    private:
        QPushButton *portPermission;
        QPushButton *startReading;
        QPushButton *quitButton;

};

#endif // WINDOW_H
