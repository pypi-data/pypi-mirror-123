Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const mobx_react_1 = require("mobx-react");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const list_1 = (0, tslib_1.__importDefault)(require("app/components/list"));
const listItem_1 = (0, tslib_1.__importDefault)(require("app/components/list/listItem"));
const panels_1 = require("app/components/panels");
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/searchBar"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const QuickTraceContext = (0, tslib_1.__importStar)(require("app/utils/performance/quickTrace/quickTraceContext"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const AnchorLinkManager = (0, tslib_1.__importStar)(require("./anchorLinkManager"));
const filter_1 = (0, tslib_1.__importDefault)(require("./filter"));
const traceView_1 = (0, tslib_1.__importDefault)(require("./traceView"));
const utils_2 = require("./utils");
const waterfallModel_1 = (0, tslib_1.__importDefault)(require("./waterfallModel"));
class SpansInterface extends react_1.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            parsedTrace: (0, utils_2.parseTrace)(this.props.event),
            waterfallModel: new waterfallModel_1.default(this.props.event),
        };
        this.handleSpanFilter = (searchQuery) => {
            const { waterfallModel } = this.state;
            waterfallModel.querySpanSearch(searchQuery);
        };
    }
    static getDerivedStateFromProps(props, state) {
        if (state.waterfallModel.isEvent(props.event)) {
            return state;
        }
        return Object.assign(Object.assign({}, state), { parsedTrace: (0, utils_2.parseTrace)(props.event), waterfallModel: new waterfallModel_1.default(props.event) });
    }
    renderTraceErrorsAlert({ isLoading, errors, parsedTrace, }) {
        if (isLoading) {
            return null;
        }
        if (!errors || errors.length <= 0) {
            return null;
        }
        const label = (0, locale_1.tn)('There is an error event associated with this transaction event.', `There are %s error events associated with this transaction event.`, errors.length);
        // mapping from span ids to the span op and the number of errors in that span
        const errorsMap = {};
        errors.forEach(error => {
            if (!errorsMap[error.span]) {
                // first check of the error belongs to the root span
                if (parsedTrace.rootSpanID === error.span) {
                    errorsMap[error.span] = {
                        operation: parsedTrace.op,
                        errorsCount: 0,
                    };
                }
                else {
                    // since it does not belong to the root span, check if it belongs
                    // to one of the other spans in the transaction
                    const span = parsedTrace.spans.find(s => s.span_id === error.span);
                    if (!(span === null || span === void 0 ? void 0 : span.op)) {
                        return;
                    }
                    errorsMap[error.span] = {
                        operation: span.op,
                        errorsCount: 0,
                    };
                }
            }
            errorsMap[error.span].errorsCount++;
        });
        return (<AlertContainer>
        <alert_1.default type="error" icon={<icons_1.IconWarning size="md"/>}>
          <ErrorLabel>{label}</ErrorLabel>
          <AnchorLinkManager.Consumer>
            {({ scrollToHash }) => (<list_1.default symbol="bullet">
                {Object.entries(errorsMap).map(([spanId, { operation, errorsCount }]) => (<listItem_1.default key={spanId}>
                    {(0, locale_1.tct)('[errors] in [link]', {
                        errors: (0, locale_1.tn)('%s error in ', '%s errors in ', errorsCount),
                        link: (<ErrorLink onClick={(0, utils_2.scrollToSpan)(spanId, scrollToHash, this.props.location)}>
                          {operation}
                        </ErrorLink>),
                    })}
                  </listItem_1.default>))}
              </list_1.default>)}
          </AnchorLinkManager.Consumer>
        </alert_1.default>
      </AlertContainer>);
    }
    render() {
        const { event, organization } = this.props;
        const { parsedTrace, waterfallModel } = this.state;
        return (<Container hasErrors={!(0, utils_1.objectIsEmpty)(event.errors)}>
        <QuickTraceContext.Consumer>
          {quickTrace => {
                var _a;
                return (<AnchorLinkManager.Provider>
              {this.renderTraceErrorsAlert({
                        isLoading: (quickTrace === null || quickTrace === void 0 ? void 0 : quickTrace.isLoading) || false,
                        errors: (_a = quickTrace === null || quickTrace === void 0 ? void 0 : quickTrace.currentEvent) === null || _a === void 0 ? void 0 : _a.errors,
                        parsedTrace,
                    })}
              <mobx_react_1.Observer>
                {() => {
                        return (<Search>
                      <filter_1.default operationNameCounts={waterfallModel.operationNameCounts} operationNameFilter={waterfallModel.operationNameFilters} toggleOperationNameFilter={waterfallModel.toggleOperationNameFilter} toggleAllOperationNameFilters={waterfallModel.toggleAllOperationNameFilters}/>
                      <StyledSearchBar defaultQuery="" query={waterfallModel.searchQuery || ''} placeholder={(0, locale_1.t)('Search for spans')} onSearch={this.handleSpanFilter}/>
                    </Search>);
                    }}
              </mobx_react_1.Observer>
              <panels_1.Panel>
                <mobx_react_1.Observer>
                  {() => {
                        return (<traceView_1.default waterfallModel={waterfallModel} organization={organization}/>);
                    }}
                </mobx_react_1.Observer>
                <GuideAnchorWrapper>
                  <guideAnchor_1.default target="span_tree" position="bottom"/>
                </GuideAnchorWrapper>
              </panels_1.Panel>
            </AnchorLinkManager.Provider>);
            }}
        </QuickTraceContext.Consumer>
      </Container>);
    }
}
const GuideAnchorWrapper = (0, styled_1.default)('div') `
  height: 0;
  width: 0;
  margin-left: 50%;
`;
const Container = (0, styled_1.default)('div') `
  ${p => p.hasErrors &&
    `
  padding: ${(0, space_1.default)(2)} 0;

  @media (min-width: ${p.theme.breakpoints[0]}) {
    padding: ${(0, space_1.default)(3)} 0 0 0;
  }
  `}
`;
const ErrorLink = (0, styled_1.default)('a') `
  color: ${p => p.theme.textColor};
  :hover {
    color: ${p => p.theme.textColor};
  }
`;
const Search = (0, styled_1.default)('div') `
  display: flex;
  width: 100%;
  margin-bottom: ${(0, space_1.default)(1)};
`;
const StyledSearchBar = (0, styled_1.default)(searchBar_1.default) `
  flex-grow: 1;
`;
const AlertContainer = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(1)};
`;
const ErrorLabel = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(1)};
`;
exports.default = (0, react_router_1.withRouter)((0, withOrganization_1.default)(SpansInterface));
//# sourceMappingURL=index.jsx.map