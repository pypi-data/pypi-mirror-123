Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const search_1 = (0, tslib_1.__importDefault)(require("app/components/search"));
const searchResult_1 = (0, tslib_1.__importDefault)(require("app/components/search/searchResult"));
const searchResultWrapper_1 = (0, tslib_1.__importDefault)(require("app/components/search/searchResultWrapper"));
const helpSource_1 = (0, tslib_1.__importDefault)(require("app/components/search/sources/helpSource"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const renderResult = ({ item, matches, itemProps, highlighted }) => {
    var _a;
    const sectionHeading = item.sectionHeading !== undefined ? (<SectionHeading>
        <icons_1.IconWindow />
        {(0, locale_1.t)('From %s', item.sectionHeading)}
        <Count>{(0, locale_1.tn)('%s result', '%s results', (_a = item.sectionCount) !== null && _a !== void 0 ? _a : 0)}</Count>
      </SectionHeading>) : null;
    if (item.empty) {
        return (<React.Fragment>
        {sectionHeading}
        <Empty>{(0, locale_1.t)('No results from %s', item.sectionHeading)}</Empty>
      </React.Fragment>);
    }
    return (<React.Fragment>
      {sectionHeading}
      <searchResultWrapper_1.default {...itemProps} highlighted={highlighted}>
        <searchResult_1.default highlighted={highlighted} item={item} matches={matches}/>
      </searchResultWrapper_1.default>
    </React.Fragment>);
};
// TODO(ts): Type based on Search props once that has types
const HelpSearch = props => (<search_1.default {...props} sources={[helpSource_1.default]} minSearch={3} closeOnSelect={false} renderItem={renderResult}/>);
const SectionHeading = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content 1fr max-content;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
  background: ${p => p.theme.backgroundSecondary};
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};

  &:not(:first-of-type) {
    border-top: 1px solid ${p => p.theme.innerBorder};
  }
`;
const Count = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeSmall};
  color: ${p => p.theme.gray300};
`;
const Empty = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  padding: ${(0, space_1.default)(2)};
  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeMedium};
  border-top: 1px solid ${p => p.theme.innerBorder};
`;
exports.default = HelpSearch;
//# sourceMappingURL=helpSearch.jsx.map