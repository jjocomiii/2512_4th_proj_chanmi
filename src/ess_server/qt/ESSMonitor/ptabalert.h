#ifndef PTABALERT_H
#define PTABALERT_H

#include <QWidget>

namespace Ui {
class pTabAlert;
}

class pTabAlert : public QWidget
{
    Q_OBJECT

public:
    explicit pTabAlert(QWidget *parent = nullptr);
    ~pTabAlert();

private:
    Ui::pTabAlert *ui;
};

#endif // PTABALERT_H
