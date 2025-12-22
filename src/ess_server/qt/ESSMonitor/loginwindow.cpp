#include "loginwindow.h"
#include "ui_loginwindow.h"
#include "mainwindow.h"

LoginWindow::LoginWindow(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::pLoginWindow)
{
    ui->setupUi(this);

     this->setWindowTitle("Login");

    connect(ui->pPBtton_Login, SIGNAL(clicked()), this, SLOT(on_pPBtton_Login_clicked()));
}

LoginWindow::~LoginWindow()
{
    delete ui;
}

void LoginWindow::on_pPBtton_Login_clicked()
{
    QString id = ui->pLineEdit_ID->text();
    QString pw = ui->pLineEdit_PW->text();

    if(id == "kcci_admin" && pw == "kcci1234")
    {
        MainWindow *pMainWindow = new MainWindow();
        pMainWindow->show();

        this->close();
    }
    else
    {
        ui->pLabel_status->setText("Login Failed. Please retry.");
    }

}

