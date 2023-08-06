Object.defineProperty(exports, "__esModule", { value: true });
exports.crashReportTypes = void 0;
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const xor_1 = (0, tslib_1.__importDefault)(require("lodash/xor"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const crashReportTypes = ['event.minidump', 'event.applecrashreport'];
exports.crashReportTypes = crashReportTypes;
const GroupEventAttachmentsFilter = (props) => {
    const { query, pathname } = props.location;
    const { types } = query;
    const allAttachmentsQuery = (0, omit_1.default)(query, 'types');
    const onlyCrashReportsQuery = Object.assign(Object.assign({}, query), { types: crashReportTypes });
    let activeButton = '';
    if (types === undefined) {
        activeButton = 'all';
    }
    else if ((0, xor_1.default)(crashReportTypes, types).length === 0) {
        activeButton = 'onlyCrash';
    }
    return (<FilterWrapper>
      <buttonBar_1.default merged active={activeButton}>
        <button_1.default barId="all" size="small" to={{ pathname, query: allAttachmentsQuery }}>
          {(0, locale_1.t)('All Attachments')}
        </button_1.default>
        <button_1.default barId="onlyCrash" size="small" to={{ pathname, query: onlyCrashReportsQuery }}>
          {(0, locale_1.t)('Only Crash Reports')}
        </button_1.default>
      </buttonBar_1.default>
    </FilterWrapper>);
};
const FilterWrapper = (0, styled_1.default)('div') `
  display: flex;
  justify-content: flex-end;
  margin-bottom: ${(0, space_1.default)(3)};
`;
exports.default = (0, react_router_1.withRouter)(GroupEventAttachmentsFilter);
//# sourceMappingURL=groupEventAttachmentsFilter.jsx.map