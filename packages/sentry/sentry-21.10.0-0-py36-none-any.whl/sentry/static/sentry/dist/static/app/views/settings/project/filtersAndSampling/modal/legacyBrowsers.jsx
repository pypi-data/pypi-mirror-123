Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const bulkController_1 = (0, tslib_1.__importDefault)(require("app/components/bulkController"));
const switchButton_1 = (0, tslib_1.__importDefault)(require("app/components/switchButton"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const dynamicSampling_1 = require("app/types/dynamicSampling");
const utils_1 = require("../utils");
const legacyBrowsers = Object.values(dynamicSampling_1.LegacyBrowser);
function LegacyBrowsers({ onChange, selectedLegacyBrowsers = [] }) {
    function handleChange({ selectedIds, }) {
        onChange(selectedIds);
    }
    return (<bulkController_1.default pageIds={legacyBrowsers} defaultSelectedIds={selectedLegacyBrowsers} allRowsCount={legacyBrowsers.length} onChange={handleChange} columnsCount={0}>
      {({ selectedIds, onRowToggle, onPageRowsToggle, isPageSelected }) => (<Wrapper>
          {(0, locale_1.t)('All browsers')}
          <switchButton_1.default key="switch" size="lg" isActive={isPageSelected} toggle={() => {
                onPageRowsToggle(!isPageSelected);
            }}/>
          {legacyBrowsers.map(legacyBrowser => {
                const { icon, title } = utils_1.LEGACY_BROWSER_LIST[legacyBrowser];
                return (<react_1.Fragment key={legacyBrowser}>
                <BrowserWrapper>
                  <Icon className={`icon-${icon}`} data-test-id={`icon-${icon}`}/>
                  {title}
                </BrowserWrapper>
                <switchButton_1.default size="lg" isActive={selectedIds.includes(legacyBrowser)} toggle={() => onRowToggle(legacyBrowser)}/>
              </react_1.Fragment>);
            })}
        </Wrapper>)}
    </bulkController_1.default>);
}
exports.default = LegacyBrowsers;
const Wrapper = (0, styled_1.default)('div') `
  grid-column: 1/-1;
  display: grid;
  grid-template-columns: 1fr max-content;
  grid-gap: ${(0, space_1.default)(2)};
  font-size: ${p => p.theme.fontSizeLarge};
  color: ${p => p.theme.gray400};
  padding-top: ${(0, space_1.default)(2)};
  padding-bottom: ${(0, space_1.default)(1)};
`;
const BrowserWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-column-gap: ${(0, space_1.default)(1)};
  color: ${p => p.theme.gray500};
`;
const Icon = (0, styled_1.default)('div') `
  width: 24px;
  height: 24px;
  background-repeat: no-repeat;
  background-position: center;
  background-size: 24px 24px;
  flex-shrink: 0;
`;
//# sourceMappingURL=legacyBrowsers.jsx.map