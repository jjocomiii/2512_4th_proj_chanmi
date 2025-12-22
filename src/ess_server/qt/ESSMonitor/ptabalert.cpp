#include "ptabalert.h"
#include "ui_ptabalert.h"

pTabAlert::pTabAlert(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::pTabAlert)
{
    ui->setupUi(this);
}

pTabAlert::~pTabAlert()
{
    delete ui;
}
