Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const locale_1 = require("app/locale");
const selectField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/selectField"));
function StepFifth({ appleStoreOrgs, stepFifthData, onSetStepFifthData }) {
    var _a, _b;
    return (<StyledSelectField name="organization" label={(0, locale_1.t)('iTunes Organization')} options={appleStoreOrgs.map(appleStoreOrg => ({
            value: appleStoreOrg.organizationId,
            label: appleStoreOrg.name,
        }))} placeholder={(0, locale_1.t)('Select organization')} onChange={organizationId => {
            const selectedAppleStoreOrg = appleStoreOrgs.find(appleStoreOrg => appleStoreOrg.organizationId === organizationId);
            onSetStepFifthData({ org: selectedAppleStoreOrg });
        }} value={(_b = (_a = stepFifthData.org) === null || _a === void 0 ? void 0 : _a.organizationId) !== null && _b !== void 0 ? _b : ''} inline={false} flexibleControlStateSize stacked required/>);
}
exports.default = StepFifth;
const StyledSelectField = (0, styled_1.default)(selectField_1.default) `
  padding-right: 0;
`;
//# sourceMappingURL=stepFifth.jsx.map