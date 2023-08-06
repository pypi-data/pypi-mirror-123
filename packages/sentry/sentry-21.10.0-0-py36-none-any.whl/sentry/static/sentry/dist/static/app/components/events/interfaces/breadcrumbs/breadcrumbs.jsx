Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_virtualized_1 = require("react-virtualized");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const panels_1 = require("app/components/panels");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const breadcrumb_1 = (0, tslib_1.__importDefault)(require("./breadcrumb"));
const PANEL_MAX_HEIGHT = 400;
const cache = new react_virtualized_1.CellMeasurerCache({
    fixedWidth: true,
    minHeight: 42,
});
function Breadcrumbs({ breadcrumbs, displayRelativeTime, onSwitchTimeFormat, organization, searchTerm, event, relativeTime, emptyMessage, route, router, }) {
    const [scrollToIndex, setScrollToIndex] = (0, react_1.useState)(undefined);
    const [scrollbarSize, setScrollbarSize] = (0, react_1.useState)(0);
    let listRef = null;
    const contentRef = (0, react_1.useRef)(null);
    (0, react_1.useEffect)(() => {
        updateGrid();
    }, []);
    (0, react_1.useEffect)(() => {
        if (!!breadcrumbs.length && !scrollToIndex) {
            setScrollToIndex(breadcrumbs.length - 1);
            return;
        }
        updateGrid();
    }, [breadcrumbs]);
    (0, react_1.useEffect)(() => {
        if (scrollToIndex !== undefined) {
            updateGrid();
        }
    }, [scrollToIndex]);
    function updateGrid() {
        if (listRef) {
            cache.clearAll();
            listRef.forceUpdateGrid();
        }
    }
    function renderRow({ index, key, parent, style }) {
        const breadcrumb = breadcrumbs[index];
        const isLastItem = breadcrumbs[breadcrumbs.length - 1].id === breadcrumb.id;
        const { height } = style;
        return (<react_virtualized_1.CellMeasurer cache={cache} columnIndex={0} key={key} parent={parent} rowIndex={index}>
        {({ measure }) => {
                var _a, _b;
                return (<breadcrumb_1.default data-test-id={isLastItem ? 'last-crumb' : 'crumb'} style={style} onLoad={measure} organization={organization} searchTerm={searchTerm} breadcrumb={breadcrumb} event={event} relativeTime={relativeTime} displayRelativeTime={displayRelativeTime} height={height ? String(height) : undefined} scrollbarSize={((_b = (_a = contentRef === null || contentRef === void 0 ? void 0 : contentRef.current) === null || _a === void 0 ? void 0 : _a.offsetHeight) !== null && _b !== void 0 ? _b : 0) < PANEL_MAX_HEIGHT
                        ? scrollbarSize
                        : 0} router={router} route={route}/>);
            }}
      </react_virtualized_1.CellMeasurer>);
    }
    return (<StyledPanelTable scrollbarSize={scrollbarSize} headers={[
            (0, locale_1.t)('Type'),
            (0, locale_1.t)('Category'),
            (0, locale_1.t)('Description'),
            (0, locale_1.t)('Level'),
            <Time key="time" onClick={onSwitchTimeFormat}>
          <tooltip_1.default containerDisplayMode="inline-flex" title={displayRelativeTime ? (0, locale_1.t)('Switch to absolute') : (0, locale_1.t)('Switch to relative')}>
            <StyledIconSwitch size="xs"/>
          </tooltip_1.default>

          {(0, locale_1.t)('Time')}
        </Time>,
            '',
        ]} isEmpty={!breadcrumbs.length} {...emptyMessage}>
      <Content ref={contentRef}>
        <react_virtualized_1.AutoSizer disableHeight onResize={updateGrid}>
          {({ width }) => (<StyledList ref={(el) => {
                listRef = el;
            }} deferredMeasurementCache={cache} height={PANEL_MAX_HEIGHT} overscanRowCount={5} rowCount={breadcrumbs.length} rowHeight={cache.rowHeight} rowRenderer={renderRow} width={width} onScrollbarPresenceChange={({ size }) => setScrollbarSize(size)} 
        // when the component mounts, it scrolls to the last item
        scrollToIndex={scrollToIndex} scrollToAlignment={scrollToIndex ? 'end' : undefined}/>)}
        </react_virtualized_1.AutoSizer>
      </Content>
    </StyledPanelTable>);
}
exports.default = Breadcrumbs;
const StyledPanelTable = (0, styled_1.default)(panels_1.PanelTable) `
  display: grid;
  grid-template-columns: 64px 140px 1fr 106px 100px ${p => `${p.scrollbarSize}px`};

  > * {
    :nth-child(-n + 6) {
      border-bottom: 1px solid ${p => p.theme.border};
      border-radius: 0;
      /* This is to fix a small issue with the border not being fully visible on smaller devices */
      margin-bottom: 1px;

      /* Type */
      :nth-child(6n-5) {
        text-align: center;
      }
    }

    /* Content */
    :nth-child(n + 7) {
      grid-column: 1/-1;
      ${p => !p.isEmpty &&
    `
          padding: 0;
        `}
    }
  }

  @media (max-width: ${props => props.theme.breakpoints[0]}) {
    grid-template-columns: 48px 1fr 74px 82px ${p => `${p.scrollbarSize}px`};
    > * {
      :nth-child(-n + 6) {
        /* Type, Category & Level */
        :nth-child(6n-5),
        :nth-child(6n-4),
        :nth-child(6n-2) {
          color: transparent;
        }

        /* Description & Scrollbar */
        :nth-child(6n-3) {
          display: none;
        }
      }
    }
  }

  overflow: hidden;
`;
const Time = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-gap: ${(0, space_1.default)(1)};
  cursor: pointer;
`;
const StyledIconSwitch = (0, styled_1.default)(icons_1.IconSwitch) `
  transition: 0.15s color;
  :hover {
    color: ${p => p.theme.gray300};
  }
`;
const Content = (0, styled_1.default)('div') `
  max-height: ${PANEL_MAX_HEIGHT}px;
  overflow: hidden;
`;
// XXX(ts): Emotion11 has some trouble with List's defaultProps
//
// It gives the list have a dynamic height; otherwise, in the case of filtered
// options, a list will be displayed with an empty space
const StyledList = (0, styled_1.default)(react_virtualized_1.List) `
  height: auto !important;
  max-height: ${p => p.height}px;
  outline: none;
`;
//# sourceMappingURL=breadcrumbs.jsx.map