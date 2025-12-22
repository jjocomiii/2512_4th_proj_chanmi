/********************************************************************************
** Form generated from reading UI file 'ptabenv.ui'
**
** Created by: Qt User Interface Compiler version 6.8.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_PTABENV_H
#define UI_PTABENV_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_pTabEnv
{
public:

    void setupUi(QWidget *pTabEnv)
    {
        if (pTabEnv->objectName().isEmpty())
            pTabEnv->setObjectName("pTabEnv");
        pTabEnv->resize(400, 300);

        retranslateUi(pTabEnv);

        QMetaObject::connectSlotsByName(pTabEnv);
    } // setupUi

    void retranslateUi(QWidget *pTabEnv)
    {
        pTabEnv->setWindowTitle(QCoreApplication::translate("pTabEnv", "Form", nullptr));
    } // retranslateUi

};

namespace Ui {
    class pTabEnv: public Ui_pTabEnv {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_PTABENV_H
