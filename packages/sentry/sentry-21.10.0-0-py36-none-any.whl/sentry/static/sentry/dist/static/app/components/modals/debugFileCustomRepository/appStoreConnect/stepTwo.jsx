Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const locale_1 = require("app/locale");
const selectField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/selectField"));
function StepTwo({ stepTwoData, onSetStepTwoData, appStoreApps }) {
    var _a, _b;
    return (<StyledSelectField name="application" label={(0, locale_1.t)('App Store Connect application')} options={appStoreApps.map(appStoreApp => ({
            value: appStoreApp.appId,
            label: appStoreApp.name,
        }))} placeholder={(0, locale_1.t)('Select application')} onChange={appId => {
            const selectedAppStoreApp = appStoreApps.find(appStoreApp => appStoreApp.appId === appId);
            onSetStepTwoData({ app: selectedAppStoreApp });
        }} value={(_b = (_a = stepTwoData.app) === null || _a === void 0 ? void 0 : _a.appId) !== null && _b !== void 0 ? _b : ''} inline={false} flexibleControlStateSize stacked required/>);
}
exports.default = StepTwo;
const StyledSelectField = (0, styled_1.default)(selectField_1.default) `
  padding-right: 0;
`;
//# sourceMappingURL=stepTwo.jsx.map