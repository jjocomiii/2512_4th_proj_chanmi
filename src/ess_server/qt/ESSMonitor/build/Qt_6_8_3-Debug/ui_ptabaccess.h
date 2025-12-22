/********************************************************************************
** Form generated from reading UI file 'ptabaccess.ui'
**
** Created by: Qt User Interface Compiler version 6.8.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_PTABACCESS_H
#define UI_PTABACCESS_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_pTabAccess
{
public:

    void setupUi(QWidget *pTabAccess)
    {
        if (pTabAccess->objectName().isEmpty())
            pTabAccess->setObjectName("pTabAccess");
        pTabAccess->resize(400, 300);

        retranslateUi(pTabAccess);

        QMetaObject::connectSlotsByName(pTabAccess);
    } // setupUi

    void retranslateUi(QWidget *pTabAccess)
    {
        pTabAccess->setWindowTitle(QCoreApplication::translate("pTabAccess", "Form", nullptr));
    } // retranslateUi

};

namespace Ui {
    class pTabAccess: public Ui_pTabAccess {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_PTABACCESS_H
