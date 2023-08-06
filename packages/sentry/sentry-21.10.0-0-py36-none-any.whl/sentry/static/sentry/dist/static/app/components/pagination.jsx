Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const parseLinkHeader_1 = (0, tslib_1.__importDefault)(require("app/utils/parseLinkHeader"));
const defaultOnCursor = (cursor, path, query, _direction) => react_router_1.browserHistory.push({
    pathname: path,
    query: Object.assign(Object.assign({}, query), { cursor }),
});
const Pagination = ({ to, location, className, onCursor = defaultOnCursor, pageLinks, size = 'small', caption, disabled = false, }) => {
    var _a, _b;
    if (!pageLinks) {
        return null;
    }
    const path = to !== null && to !== void 0 ? to : location.pathname;
    const query = location.query;
    const links = (0, parseLinkHeader_1.default)(pageLinks);
    const previousDisabled = disabled || ((_a = links.previous) === null || _a === void 0 ? void 0 : _a.results) === false;
    const nextDisabled = disabled || ((_b = links.next) === null || _b === void 0 ? void 0 : _b.results) === false;
    return (<Wrapper className={className}>
      {caption && <PaginationCaption>{caption}</PaginationCaption>}
      <buttonBar_1.default merged>
        <button_1.default icon={<icons_1.IconChevron direction="left" size="sm"/>} aria-label={(0, locale_1.t)('Previous')} size={size} disabled={previousDisabled} onClick={() => { var _a; return onCursor === null || onCursor === void 0 ? void 0 : onCursor((_a = links.previous) === null || _a === void 0 ? void 0 : _a.cursor, path, query, -1); }}/>
        <button_1.default icon={<icons_1.IconChevron direction="right" size="sm"/>} aria-label={(0, locale_1.t)('Next')} size={size} disabled={nextDisabled} onClick={() => { var _a; return onCursor === null || onCursor === void 0 ? void 0 : onCursor((_a = links.next) === null || _a === void 0 ? void 0 : _a.cursor, path, query, 1); }}/>
      </buttonBar_1.default>
    </Wrapper>);
};
const Wrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin: ${(0, space_1.default)(3)} 0 0 0;
`;
const PaginationCaption = (0, styled_1.default)('span') `
  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeMedium};
  margin-right: ${(0, space_1.default)(2)};
`;
exports.default = (0, react_router_1.withRouter)(Pagination);
//# sourceMappingURL=pagination.jsx.map