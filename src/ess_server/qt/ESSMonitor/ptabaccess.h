#ifndef PTABACCESS_H
#define PTABACCESS_H

#include <QWidget>

namespace Ui {
class pTabAccess;
}

class pTabAccess : public QWidget
{
    Q_OBJECT

public:
    explicit pTabAccess(QWidget *parent = nullptr);
    ~pTabAccess();

private:
    Ui::pTabAccess *ui;
};

#endif // PTABACCESS_H
