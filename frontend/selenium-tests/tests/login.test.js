const { Builder, By, until } = require('selenium-webdriver');
const { expect } = require('chai');
const config = require('../config');
const LoginPage = require('../pages/loginPage');

describe('Smile App Web Frontend - Authentication & Login E2E Selenium Suite', function () {
    this.timeout(30000);
    let driver;
    let loginPage;

    beforeEach(async function () {
        driver = await new Builder().forBrowser(config.BROWSER).build();
        loginPage = new LoginPage(driver);
        await loginPage.openApp();
    });

    afterEach(async function () {
        if (driver) {
            await driver.quit();
        }
    });

    it('TC_WEB_001: Should display Start screen with Patient and Doctor role selection buttons', async function () {
        const startScreen = await driver.findElement(By.id('screen-start'));
        const isVisible = await startScreen.isDisplayed();
        expect(isVisible).to.be.true;

        const patientBtn = await driver.findElement(loginPage.btnPatientRole);
        const doctorBtn = await driver.findElement(loginPage.btnDoctorRole);

        expect(await patientBtn.isDisplayed()).to.be.true;
        expect(await doctorBtn.isDisplayed()).to.be.true;
    });

    it('TC_WEB_002: Should navigate to Patient Login screen when clicking I\'M A PATIENT', async function () {
        await loginPage.selectPatientRole();
        const childLoginScreen = await driver.findElement(loginPage.screenLoginChild);
        expect(await childLoginScreen.isDisplayed()).to.be.true;
    });

    it('TC_WEB_003: Should navigate to Doctor Login screen when clicking I\'M A DOCTOR', async function () {
        await loginPage.selectDoctorRole();
        const doctorLoginScreen = await driver.findElement(loginPage.screenLoginDoctor);
        expect(await doctorLoginScreen.isDisplayed()).to.be.true;
    });

    it('TC_WEB_004: Patient Login - Should accept input email and password credentials', async function () {
        await loginPage.selectPatientRole();
        await loginPage.loginAsPatient(config.TEST_USERS.PATIENT.email, config.TEST_USERS.PATIENT.password);
        
        const emailVal = await driver.findElement(loginPage.inputChildEmail).getAttribute('value');
        expect(emailVal).to.equal(config.TEST_USERS.PATIENT.email);
    });

    it('TC_WEB_005: Doctor Login - Should accept input email and password credentials', async function () {
        await loginPage.selectDoctorRole();
        await loginPage.loginAsDoctor(config.TEST_USERS.DOCTOR.email, config.TEST_USERS.DOCTOR.password);

        const emailVal = await driver.findElement(loginPage.inputDoctorEmail).getAttribute('value');
        expect(emailVal).to.equal(config.TEST_USERS.DOCTOR.email);
    });

    it('TC_WEB_006: Registration - Should show Doctor ID field when Patient role is selected', async function () {
        await loginPage.selectPatientRole();
        const signUpLink = await driver.findElement(By.xpath("//span[contains(text(), 'Sign Up')]"));
        await signUpLink.click();

        const doctorIdField = await driver.findElement(By.id('doctor-id-field'));
        expect(await doctorIdField.isDisplayed()).to.be.true;
    });

    it('TC_WEB_007: Registration - Should hide Doctor ID field when Doctor role tab is toggled', async function () {
        await loginPage.selectPatientRole();
        const signUpLink = await driver.findElement(By.xpath("//span[contains(text(), 'Sign Up')]"));
        await signUpLink.click();

        await loginPage.fillRegistrationForm('Dr. Test', 'drtest@example.com', 'Pass123!', 'doctor');
        const doctorIdField = await driver.findElement(By.id('doctor-id-field'));
        expect(await doctorIdField.isDisplayed()).to.be.false;
    });
});
