Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const alertLink_1 = (0, tslib_1.__importDefault)(require("app/components/alertLink"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const utils_1 = require("app/components/projects/appStoreConnectContext/utils");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const stepFifth_1 = (0, tslib_1.__importDefault)(require("./stepFifth"));
const stepFour_1 = (0, tslib_1.__importDefault)(require("./stepFour"));
const stepOne_1 = (0, tslib_1.__importDefault)(require("./stepOne"));
const stepThree_1 = (0, tslib_1.__importDefault)(require("./stepThree"));
const stepTwo_1 = (0, tslib_1.__importDefault)(require("./stepTwo"));
const utils_2 = require("./utils");
const steps = [
    (0, locale_1.t)('App Store Connect credentials'),
    (0, locale_1.t)('Choose an application'),
    (0, locale_1.t)('Enter iTunes credentials'),
    (0, locale_1.t)('Enter authentication code'),
    (0, locale_1.t)('Choose an organization'),
];
function AppStoreConnect({ Header, Body, Footer, api, initialData, orgSlug, projectSlug, onSubmit, location, appStoreConnectContext, }) {
    const { updateAlertMessage } = appStoreConnectContext !== null && appStoreConnectContext !== void 0 ? appStoreConnectContext : {};
    const [revalidateItunesSession, setRevalidateItunesSession] = (0, react_1.useState)(location.query.revalidateItunesSession);
    const [isLoading, setIsLoading] = (0, react_1.useState)(false);
    const [activeStep, setActiveStep] = (0, react_1.useState)(revalidateItunesSession ? 3 : 0);
    const [appStoreApps, setAppStoreApps] = (0, react_1.useState)([]);
    const [appleStoreOrgs, setAppleStoreOrgs] = (0, react_1.useState)([]);
    const [sessionContext, setSessionContext] = (0, react_1.useState)(undefined);
    const [stepOneData, setStepOneData] = (0, react_1.useState)({
        issuer: initialData === null || initialData === void 0 ? void 0 : initialData.appconnectIssuer,
        keyId: initialData === null || initialData === void 0 ? void 0 : initialData.appconnectKey,
        privateKey: typeof (initialData === null || initialData === void 0 ? void 0 : initialData.appconnectPrivateKey) === 'object' ? undefined : '',
    });
    const [stepTwoData, setStepTwoData] = (0, react_1.useState)({
        app: (initialData === null || initialData === void 0 ? void 0 : initialData.appId) && (initialData === null || initialData === void 0 ? void 0 : initialData.appName)
            ? {
                appId: initialData.appId,
                name: initialData.appName,
                bundleId: initialData.bundleId,
            }
            : undefined,
    });
    const [stepThreeData, setStepThreeData] = (0, react_1.useState)({
        username: initialData === null || initialData === void 0 ? void 0 : initialData.itunesUser,
        password: typeof (initialData === null || initialData === void 0 ? void 0 : initialData.itunesPassword) === 'object' ? undefined : '',
    });
    const [stepFourData, setStepFourData] = (0, react_1.useState)({
        authenticationCode: undefined,
    });
    const [stepFifthData, setStepFifthData] = (0, react_1.useState)({
        org: (initialData === null || initialData === void 0 ? void 0 : initialData.orgPublicId) && (initialData === null || initialData === void 0 ? void 0 : initialData.name)
            ? { organizationId: initialData.orgPublicId, name: initialData.name }
            : undefined,
    });
    (0, react_1.useEffect)(() => {
        if (location.query.revalidateItunesSession && !revalidateItunesSession) {
            setIsLoading(true);
            setRevalidateItunesSession(location.query.revalidateItunesSession);
        }
    }, [location.query]);
    (0, react_1.useEffect)(() => {
        if (revalidateItunesSession) {
            handleStartItunesAuthentication(false);
            if (activeStep !== 3) {
                setActiveStep(3);
            }
            setIsLoading(false);
            return;
        }
        setIsLoading(false);
    }, [revalidateItunesSession]);
    function checkAppStoreConnectCredentials() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            setIsLoading(true);
            try {
                const response = yield api.requestPromise(`/projects/${orgSlug}/${projectSlug}/appstoreconnect/apps/`, {
                    method: 'POST',
                    data: {
                        id: stepOneData.privateKey !== undefined ? undefined : initialData === null || initialData === void 0 ? void 0 : initialData.id,
                        appconnectIssuer: stepOneData.issuer,
                        appconnectKey: stepOneData.keyId,
                        appconnectPrivateKey: stepOneData.privateKey,
                    },
                });
                setAppStoreApps(response.apps);
                setStepTwoData({ app: response.apps[0] });
                setIsLoading(false);
                goNext();
            }
            catch (error) {
                setIsLoading(false);
                // app-connect-authentication-error
                (0, indicator_1.addErrorMessage)((0, utils_2.getAppStoreErrorMessage)(error));
            }
        });
    }
    function startTwoFactorAuthentication(shouldJumpNext = false) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            setIsLoading(true);
            try {
                const response = yield api.requestPromise(`/projects/${orgSlug}/${projectSlug}/appstoreconnect/2fa/`, {
                    method: 'POST',
                    data: {
                        code: stepFourData.authenticationCode,
                        sessionContext,
                    },
                });
                const { organizations, sessionContext: newSessionContext } = response;
                if (shouldJumpNext) {
                    persistData(newSessionContext);
                    return;
                }
                setSessionContext(newSessionContext);
                setAppleStoreOrgs(organizations);
                setStepFifthData({ org: organizations[0] });
                setIsLoading(false);
                goNext();
            }
            catch (error) {
                setIsLoading(false);
                // itunes-2fa-required
                (0, indicator_1.addErrorMessage)((0, utils_2.getAppStoreErrorMessage)(error));
            }
        });
    }
    function persistData(newSessionContext) {
        var _a, _b;
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (!stepTwoData.app || !stepFifthData.org || !stepThreeData.username) {
                return;
            }
            setIsLoading(true);
            let endpoint = `/projects/${orgSlug}/${projectSlug}/appstoreconnect/`;
            let errorMessage = (0, locale_1.t)('An error occurred while adding the custom repository');
            let successMessage = (0, locale_1.t)('Successfully added custom repository');
            if (!!initialData) {
                endpoint = `${endpoint}${initialData.id}/`;
                errorMessage = (0, locale_1.t)('An error occurred while updating the custom repository');
                successMessage = (0, locale_1.t)('Successfully updated custom repository');
            }
            try {
                yield api.requestPromise(endpoint, {
                    method: 'POST',
                    data: {
                        itunesUser: stepThreeData.username,
                        itunesPassword: stepThreeData.password,
                        appconnectIssuer: stepOneData.issuer,
                        appconnectKey: stepOneData.keyId,
                        appconnectPrivateKey: stepOneData.privateKey,
                        appName: stepTwoData.app.name,
                        appId: stepTwoData.app.appId,
                        bundleId: stepTwoData.app.bundleId,
                        orgId: stepFifthData.org.organizationId,
                        orgName: stepFifthData.org.name,
                        sessionContext: newSessionContext !== null && newSessionContext !== void 0 ? newSessionContext : sessionContext,
                    },
                });
                (0, indicator_1.addSuccessMessage)(successMessage);
                onSubmit();
            }
            catch (error) {
                setIsLoading(false);
                if (typeof error !== 'string' &&
                    ((_b = (_a = error.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) === null || _b === void 0 ? void 0 : _b.code) ===
                        'app-connect-multiple-sources-error') {
                    (0, indicator_1.addErrorMessage)((0, utils_2.getAppStoreErrorMessage)(error));
                    return;
                }
                (0, indicator_1.addErrorMessage)(errorMessage);
            }
        });
    }
    function isFormInvalid() {
        switch (activeStep) {
            case 0:
                return Object.keys(stepOneData).some(key => {
                    if (key === 'privateKey' && stepOneData[key] === undefined) {
                        return false;
                    }
                    return !stepOneData[key];
                });
            case 1:
                return Object.keys(stepTwoData).some(key => !stepTwoData[key]);
            case 2: {
                return Object.keys(stepThreeData).some(key => {
                    if (key === 'password' && stepThreeData[key] === undefined) {
                        return false;
                    }
                    return !stepThreeData[key];
                });
            }
            case 3: {
                return Object.keys(stepFourData).some(key => !stepFourData[key]);
            }
            case 4: {
                return Object.keys(stepFifthData).some(key => !stepFifthData[key]);
            }
            default:
                return false;
        }
    }
    function goNext() {
        setActiveStep(activeStep + 1);
    }
    function handleStartItunesAuthentication(shouldGoNext = true) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (shouldGoNext) {
                setIsLoading(true);
            }
            try {
                const response = yield api.requestPromise(`/projects/${orgSlug}/${projectSlug}/appstoreconnect/start/`, {
                    method: 'POST',
                    data: {
                        id: stepThreeData.password !== undefined ? undefined : initialData === null || initialData === void 0 ? void 0 : initialData.id,
                        itunesUser: stepThreeData.username,
                        itunesPassword: stepThreeData.password,
                    },
                });
                setSessionContext(response.sessionContext);
                if (shouldGoNext) {
                    setIsLoading(false);
                    goNext();
                    return;
                }
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('An iTunes verification code has been sent'));
            }
            catch (error) {
                if (shouldGoNext) {
                    setIsLoading(false);
                }
                // itunes-authentication-error'
                (0, indicator_1.addErrorMessage)((0, utils_2.getAppStoreErrorMessage)(error));
            }
        });
    }
    function handleStartSmsAuthentication() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            try {
                const response = yield api.requestPromise(`/projects/${orgSlug}/${projectSlug}/appstoreconnect/requestSms/`, {
                    method: 'POST',
                    data: { sessionContext },
                });
                setSessionContext(response.sessionContext);
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)("We've sent a SMS code to your phone"));
            }
            catch (error) {
                // itunes-sms-blocked-error
                (0, indicator_1.addErrorMessage)((0, utils_2.getAppStoreErrorMessage)(error));
            }
        });
    }
    function handleGoBack() {
        const newActiveStep = activeStep - 1;
        switch (newActiveStep) {
            case 3:
                handleStartItunesAuthentication(false);
                setStepFourData({ authenticationCode: undefined });
                break;
            default:
                break;
        }
        setActiveStep(newActiveStep);
    }
    function handleGoNext() {
        switch (activeStep) {
            case 0:
                checkAppStoreConnectCredentials();
                break;
            case 1:
                goNext();
                break;
            case 2:
                handleStartItunesAuthentication();
                break;
            case 3:
                startTwoFactorAuthentication();
                break;
            case 4:
                persistData();
                break;
            default:
                break;
        }
    }
    function renderCurrentStep() {
        switch (activeStep) {
            case 0:
                return <stepOne_1.default stepOneData={stepOneData} onSetStepOneData={setStepOneData}/>;
            case 1:
                return (<stepTwo_1.default appStoreApps={appStoreApps} stepTwoData={stepTwoData} onSetStepTwoData={setStepTwoData}/>);
            case 2:
                return (<stepThree_1.default stepThreeData={stepThreeData} onSetStepOneData={setStepThreeData}/>);
            case 3:
                return (<stepFour_1.default stepFourData={stepFourData} onSetStepFourData={setStepFourData} onStartItunesAuthentication={handleStartItunesAuthentication} onStartSmsAuthentication={handleStartSmsAuthentication}/>);
            case 4:
                return (<stepFifth_1.default appleStoreOrgs={appleStoreOrgs} stepFifthData={stepFifthData} onSetStepFifthData={setStepFifthData}/>);
            default:
                return (<alert_1.default type="error" icon={<icons_1.IconWarning />}>
            {(0, locale_1.t)('This step could not be found.')}
          </alert_1.default>);
        }
    }
    function getAlerts() {
        const alerts = [];
        if (revalidateItunesSession) {
            if (!updateAlertMessage && revalidateItunesSession) {
                alerts.push(<StyledAlert type="warning" icon={<icons_1.IconWarning />}>
            {(0, locale_1.t)('Your iTunes session has already been re-validated.')}
          </StyledAlert>);
            }
            return alerts;
        }
        if (activeStep !== 0) {
            return alerts;
        }
        if (updateAlertMessage === utils_1.appStoreConnectAlertMessage.appStoreCredentialsInvalid) {
            alerts.push(<StyledAlert type="warning" icon={<icons_1.IconWarning />}>
          {(0, locale_1.t)('Your App Store Connect credentials are invalid. To reconnect, update your credentials.')}
        </StyledAlert>);
        }
        if (updateAlertMessage === utils_1.appStoreConnectAlertMessage.iTunesSessionInvalid) {
            alerts.push(<alertLink_1.default withoutMarginBottom icon={<icons_1.IconWarning />} to={{
                    pathname: location.pathname,
                    query: Object.assign(Object.assign({}, location.query), { revalidateItunesSession: true }),
                }}>
          {(0, locale_1.t)('Your iTunes session has expired. To reconnect, revalidate the session.')}
        </alertLink_1.default>);
        }
        return alerts;
    }
    function renderBodyContent() {
        const alerts = getAlerts();
        return (<react_1.Fragment>
        {!!alerts.length && (<Alerts marginBottom={activeStep === 3 ? 1.5 : 3}>
            {alerts.map((alert, index) => (<react_1.Fragment key={index}>{alert}</react_1.Fragment>))}
          </Alerts>)}
        {renderCurrentStep()}
      </react_1.Fragment>);
    }
    if (initialData && !appStoreConnectContext) {
        return <loadingIndicator_1.default />;
    }
    if (revalidateItunesSession) {
        return (<react_1.Fragment>
        <Header closeButton>
          <HeaderContentTitle>{(0, locale_1.t)('Revalidate iTunes session')}</HeaderContentTitle>
        </Header>
        <Body>{renderBodyContent()}</Body>
        <Footer>
          <StyledButton priority="primary" onClick={() => startTwoFactorAuthentication(true)} disabled={isLoading || isFormInvalid()}>
            {(0, locale_1.t)('Revalidate')}
          </StyledButton>
        </Footer>
      </react_1.Fragment>);
    }
    return (<react_1.Fragment>
      <Header closeButton>
        <HeaderContent>
          <NumericSymbol>{activeStep + 1}</NumericSymbol>
          <HeaderContentTitle>{steps[activeStep]}</HeaderContentTitle>
          <StepsOverview>
            {(0, locale_1.tct)('[currentStep] of [totalSteps]', {
            currentStep: activeStep + 1,
            totalSteps: steps.length,
        })}
          </StepsOverview>
        </HeaderContent>
      </Header>
      <Body>{renderBodyContent()}</Body>
      <Footer>
        <buttonBar_1.default gap={1}>
          {activeStep !== 0 && <button_1.default onClick={handleGoBack}>{(0, locale_1.t)('Back')}</button_1.default>}
          <StyledButton priority="primary" onClick={handleGoNext} disabled={isLoading || isFormInvalid()}>
            {isLoading && (<LoadingIndicatorWrapper>
                <loadingIndicator_1.default mini/>
              </LoadingIndicatorWrapper>)}
            {activeStep + 1 === steps.length
            ? initialData
                ? (0, locale_1.t)('Update')
                : (0, locale_1.t)('Save')
            : steps[activeStep + 1]}
          </StyledButton>
        </buttonBar_1.default>
      </Footer>
    </react_1.Fragment>);
}
exports.default = (0, withApi_1.default)(AppStoreConnect);
const HeaderContent = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content max-content 1fr;
  align-items: center;
  grid-gap: ${(0, space_1.default)(1)};
`;
const NumericSymbol = (0, styled_1.default)('div') `
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  font-weight: 700;
  font-size: ${p => p.theme.fontSizeMedium};
  background-color: ${p => p.theme.yellow300};
`;
const HeaderContentTitle = (0, styled_1.default)('div') `
  font-weight: 700;
  font-size: ${p => p.theme.fontSizeExtraLarge};
`;
const StepsOverview = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
  display: flex;
  justify-content: flex-end;
`;
const LoadingIndicatorWrapper = (0, styled_1.default)('div') `
  height: 100%;
  position: absolute;
  width: 100%;
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
`;
const StyledButton = (0, styled_1.default)(button_1.default) `
  position: relative;
`;
const Alerts = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1.5)};
  margin-bottom: ${p => (0, space_1.default)(p.marginBottom)};
`;
const StyledAlert = (0, styled_1.default)(alert_1.default) `
  margin: 0;
`;
//# sourceMappingURL=index.jsx.map