#include "ptabmain.h"
#include "ui_ptabmain.h"

pTabMain::pTabMain(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::pTabMain)
{
    ui->setupUi(this);
}

pTabMain::~pTabMain()
{
    delete ui;
}
