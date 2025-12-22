#include "ptabaccess.h"
#include "ui_ptabaccess.h"

pTabAccess::pTabAccess(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::pTabAccess)
{
    ui->setupUi(this);
}

pTabAccess::~pTabAccess()
{
    delete ui;
}
