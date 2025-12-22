#ifndef PTABENV_H
#define PTABENV_H

#include <QWidget>

namespace Ui {
class pTabEnv;
}

class pTabEnv : public QWidget
{
    Q_OBJECT

public:
    explicit pTabEnv(QWidget *parent = nullptr);
    ~pTabEnv();

private:
    Ui::pTabEnv *ui;
};

#endif // PTABENV_H
