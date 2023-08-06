Object.defineProperty(exports, "__esModule", { value: true });
exports.PanelTableHeader = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const is_prop_valid_1 = (0, tslib_1.__importDefault)(require("@emotion/is-prop-valid"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const panel_1 = (0, tslib_1.__importDefault)(require("./panel"));
/**
 * Bare bones table generates a CSS grid template based on the content.
 *
 * The number of children elements should be a multiple of `this.props.columns` to have
 * it look ok.
 *
 *
 * Potential customizations:
 * - [ ] Add borders for columns to make them more like cells
 * - [ ] Add prop to disable borders for rows
 * - [ ] We may need to wrap `children` with our own component (similar to what we're doing
 *       with `headers`. Then we can get rid of that gross `> *` selector
 * - [ ] Allow customization of wrappers (Header and body cells if added)
 */
const PanelTable = (_a) => {
    var { headers, children, isLoading, isEmpty, disablePadding, className, emptyMessage = (0, locale_1.t)('There are no items to display'), emptyAction, loader } = _a, props = (0, tslib_1.__rest)(_a, ["headers", "children", "isLoading", "isEmpty", "disablePadding", "className", "emptyMessage", "emptyAction", "loader"]);
    const shouldShowLoading = isLoading === true;
    const shouldShowEmptyMessage = !shouldShowLoading && isEmpty;
    const shouldShowContent = !shouldShowLoading && !shouldShowEmptyMessage;
    return (<Wrapper columns={headers.length} disablePadding={disablePadding} className={className} hasRows={shouldShowContent} {...props}>
      {headers.map((header, i) => (<exports.PanelTableHeader key={i}>{header}</exports.PanelTableHeader>))}

      {shouldShowLoading && (<LoadingWrapper>{loader || <loadingIndicator_1.default />}</LoadingWrapper>)}

      {shouldShowEmptyMessage && (<TableEmptyStateWarning>
          <p>{emptyMessage}</p>
          {emptyAction}
        </TableEmptyStateWarning>)}

      {shouldShowContent && getContent(children)}
    </Wrapper>);
};
function getContent(children) {
    if (typeof children === 'function') {
        return children();
    }
    return children;
}
const LoadingWrapper = (0, styled_1.default)('div') ``;
const TableEmptyStateWarning = (0, styled_1.default)(emptyStateWarning_1.default) ``;
const Wrapper = (0, styled_1.default)(panel_1.default, {
    shouldForwardProp: p => typeof p === 'string' && (0, is_prop_valid_1.default)(p) && p !== 'columns',
}) `
  display: grid;
  grid-template-columns: repeat(${p => p.columns}, auto);

  > * {
    ${p => (p.disablePadding ? '' : `padding: ${(0, space_1.default)(2)};`)}

    &:nth-last-child(n + ${p => (p.hasRows ? p.columns + 1 : 0)}) {
      border-bottom: 1px solid ${p => p.theme.border};
    }
  }

  > ${ /* sc-selector */TableEmptyStateWarning}, > ${ /* sc-selector */LoadingWrapper} {
    border: none;
    grid-column: auto / span ${p => p.columns};
  }

  /* safari needs an overflow value or the contents will spill out */
  overflow: auto;
`;
exports.PanelTableHeader = (0, styled_1.default)('div') `
  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeSmall};
  font-weight: 600;
  text-transform: uppercase;
  border-radius: ${p => p.theme.borderRadius} ${p => p.theme.borderRadius} 0 0;
  background: ${p => p.theme.backgroundSecondary};
  line-height: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 45px;
`;
exports.default = PanelTable;
//# sourceMappingURL=panelTable.jsx.map