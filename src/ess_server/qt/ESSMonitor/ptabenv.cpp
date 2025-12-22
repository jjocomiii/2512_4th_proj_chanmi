#include "ptabenv.h"
#include "ui_ptabenv.h"

pTabEnv::pTabEnv(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::pTabEnv)
{
    ui->setupUi(this);
}

pTabEnv::~pTabEnv()
{
    delete ui;
}
