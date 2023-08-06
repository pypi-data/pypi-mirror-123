Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const menu_1 = require("app/components/dropdownAutoComplete/menu");
const index_1 = require("app/components/organizations/timeRangeSelector/index");
function getMediaQueryForSpacer(p) {
    return p.isSpacer
        ? (0, react_1.css) `
        @media (max-width: ${p.theme.breakpoints[1]}) {
          display: none;
        }
      `
        : '';
}
const HeaderItemPosition = (0, styled_1.default)('div') `
  display: flex;
  flex: 1;
  min-width: 0;
  height: 100%;

  ${getMediaQueryForSpacer}

  ${menu_1.AutoCompleteRoot}, ${index_1.TimeRangeRoot} {
    flex: 1;
    min-width: 0;
  }
`;
exports.default = HeaderItemPosition;
//# sourceMappingURL=headerItemPosition.jsx.map