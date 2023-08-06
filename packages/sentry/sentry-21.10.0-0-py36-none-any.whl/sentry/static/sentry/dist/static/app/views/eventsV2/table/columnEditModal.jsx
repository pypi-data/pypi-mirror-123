Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const utils_1 = require("app/views/eventsV2/utils");
const columnEditCollection_1 = (0, tslib_1.__importDefault)(require("./columnEditCollection"));
class ColumnEditModal extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            columns: this.props.columns,
        };
        this.handleChange = (columns) => {
            this.setState({ columns });
        };
        this.handleApply = () => {
            this.props.onApply(this.state.columns);
            this.props.closeModal();
        };
    }
    componentDidMount() {
        const { organization } = this.props;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'discover_v2.column_editor.open',
            eventName: 'Discoverv2: Open column editor',
            organization_id: parseInt(organization.id, 10),
        });
    }
    render() {
        const { Header, Body, Footer, tagKeys, measurementKeys, spanOperationBreakdownKeys, organization, } = this.props;
        const fieldOptions = (0, utils_1.generateFieldOptions)({
            organization,
            tagKeys,
            measurementKeys,
            spanOperationBreakdownKeys,
        });
        return (<react_1.Fragment>
        <Header closeButton>
          <h4>{(0, locale_1.t)('Edit Columns')}</h4>
        </Header>
        <Body>
          <Instruction>
            {(0, locale_1.tct)('To group events, add [functionLink: functions] f(x) that may take in additional parameters. [tagFieldLink: Tag and field] columns will help you view more details about the events (i.e. title).', {
                functionLink: (<externalLink_1.default href="https://docs.sentry.io/product/discover-queries/query-builder/#filter-by-table-columns"/>),
                tagFieldLink: (<externalLink_1.default href="https://docs.sentry.io/product/sentry-basics/search/#event-properties"/>),
            })}
          </Instruction>
          <columnEditCollection_1.default columns={this.state.columns} fieldOptions={fieldOptions} onChange={this.handleChange} organization={organization}/>
        </Body>
        <Footer>
          <buttonBar_1.default gap={1}>
            <button_1.default priority="default" href={constants_1.DISCOVER2_DOCS_URL} external>
              {(0, locale_1.t)('Read the Docs')}
            </button_1.default>
            <button_1.default label={(0, locale_1.t)('Apply')} priority="primary" onClick={this.handleApply}>
              {(0, locale_1.t)('Apply')}
            </button_1.default>
          </buttonBar_1.default>
        </Footer>
      </react_1.Fragment>);
    }
}
const Instruction = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(4)};
`;
const modalCss = (0, react_2.css) `
  @media (min-width: ${theme_1.default.breakpoints[1]}) {
    width: auto;
    max-width: 900px;
  }
`;
exports.modalCss = modalCss;
exports.default = ColumnEditModal;
//# sourceMappingURL=columnEditModal.jsx.map