Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const button_1 = (0, tslib_1.__importDefault)(require("../button"));
const panels_1 = require("../panels");
function getSelectAllText(allRowsCount, bulkLimit) {
    if (!(0, utils_1.defined)(allRowsCount)) {
        return {
            noticeText: (0, locale_1.t)('Selected all items across all pages.'),
            actionText: (0, locale_1.t)('Select all items across all pages.'),
        };
    }
    if (bulkLimit && allRowsCount > bulkLimit) {
        return {
            noticeText: (0, locale_1.tct)('Selected up to the first [count] items.', {
                count: bulkLimit,
            }),
            actionText: (0, locale_1.tct)('Select the first [count] items.', {
                count: bulkLimit,
            }),
        };
    }
    return {
        noticeText: (0, locale_1.tct)('Selected all [count] items.', {
            count: allRowsCount,
        }),
        actionText: (0, locale_1.tct)('Select all [count] items.', {
            count: allRowsCount,
        }),
    };
}
function BulkNotice({ selectedRowsCount, columnsCount, isPageSelected, isAllSelected, onSelectAllRows, onUnselectAllRows, bulkLimit, allRowsCount, className, }) {
    if ((allRowsCount && allRowsCount <= selectedRowsCount) || !isPageSelected) {
        return null;
    }
    const { noticeText, actionText } = getSelectAllText(allRowsCount, bulkLimit);
    return (<Wrapper columnsCount={columnsCount} className={className}>
      {isAllSelected ? (<React.Fragment>
          {noticeText}{' '}
          <AlertButton priority="link" onClick={onUnselectAllRows}>
            {(0, locale_1.t)('Cancel selection.')}
          </AlertButton>
        </React.Fragment>) : (<React.Fragment>
          {(0, locale_1.tn)('%s item on this page selected.', '%s items on this page selected.', selectedRowsCount)}{' '}
          <AlertButton priority="link" onClick={onSelectAllRows}>
            {actionText}
          </AlertButton>
        </React.Fragment>)}
    </Wrapper>);
}
const Wrapper = (0, styled_1.default)((_a) => {
    var { columnsCount: _columnsCount } = _a, props = (0, tslib_1.__rest)(_a, ["columnsCount"]);
    return (<panels_1.PanelAlert {...props}/>);
}) `
  grid-column: span ${p => p.columnsCount};
  text-align: center;
`;
const AlertButton = (0, styled_1.default)(button_1.default) `
  &,
  &:hover,
  &:active,
  &:focus {
    /* match the styles of an <a> tag inside Alert */
    color: ${p => p.theme.textColor};
    border: none;
    border-radius: 0;
    border-bottom: 1px dotted ${p => p.theme.textColor};
    padding-bottom: 1px;
    font-size: 15px;
  }
`;
exports.default = BulkNotice;
//# sourceMappingURL=bulkNotice.jsx.map