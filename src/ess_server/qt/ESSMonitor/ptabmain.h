#ifndef PTABMAIN_H
#define PTABMAIN_H

#include <QWidget>

namespace Ui {
class pTabMain;
}

class pTabMain : public QWidget
{
    Q_OBJECT

public:
    explicit pTabMain(QWidget *parent = nullptr);
    ~pTabMain();

private:
    Ui::pTabMain *ui;
};

#endif // PTABMAIN_H
