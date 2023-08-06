Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
// This is required to offer components that sit between this settings header
// and i.e. dropdowns, some zIndex layer room
//
// e.g. app/views/settings/incidentRules/triggers/chart/
const HEADER_Z_INDEX_OFFSET = 5;
const SettingsHeader = (0, styled_1.default)('div') `
  position: sticky;
  top: 0;
  z-index: ${p => p.theme.zIndex.header + HEADER_Z_INDEX_OFFSET};
  padding: ${(0, space_1.default)(3)} ${(0, space_1.default)(4)};
  border-bottom: 1px solid ${p => p.theme.border};
  background: ${p => p.theme.background};
  height: ${p => p.theme.settings.headerHeight};
`;
exports.default = SettingsHeader;
//# sourceMappingURL=settingsHeader.jsx.map