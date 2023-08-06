Object.defineProperty(exports, "__esModule", { value: true });
exports.GroupingConfigItem = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const groupingConfigSelect_1 = (0, tslib_1.__importDefault)(require("./groupingConfigSelect"));
const groupingVariant_1 = (0, tslib_1.__importDefault)(require("./groupingVariant"));
class EventGroupingInfo extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.toggle = () => {
            this.setState(state => ({
                isOpen: !state.isOpen,
                configOverride: state.isOpen ? null : state.configOverride,
            }));
        };
        this.handleConfigSelect = selection => {
            this.setState({ configOverride: selection.value }, () => this.reloadData());
        };
    }
    getEndpoints() {
        var _a;
        const { organization, event, projectId } = this.props;
        let path = `/projects/${organization.slug}/${projectId}/events/${event.id}/grouping-info/`;
        if ((_a = this.state) === null || _a === void 0 ? void 0 : _a.configOverride) {
            path = `${path}?config=${this.state.configOverride}`;
        }
        return [['groupInfo', path]];
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { isOpen: false, configOverride: null });
    }
    renderGroupInfoSummary() {
        const { groupInfo } = this.state;
        if (!groupInfo) {
            return null;
        }
        const groupedBy = Object.values(groupInfo)
            .filter(variant => variant.hash !== null && variant.description !== null)
            .map(variant => variant.description)
            .sort((a, b) => a.toLowerCase().localeCompare(b.toLowerCase()))
            .join(', ');
        return (<SummaryGroupedBy data-test-id="loaded-grouping-info">{`(${(0, locale_1.t)('grouped by')} ${groupedBy || (0, locale_1.t)('nothing')})`}</SummaryGroupedBy>);
    }
    renderGroupConfigSelect() {
        const { configOverride } = this.state;
        const { event } = this.props;
        const configId = configOverride !== null && configOverride !== void 0 ? configOverride : event.groupingConfig.id;
        return (<GroupConfigWrapper>
        <groupingConfigSelect_1.default eventConfigId={event.groupingConfig.id} configId={configId} onSelect={this.handleConfigSelect}/>
      </GroupConfigWrapper>);
    }
    renderGroupInfo() {
        const { groupInfo, loading } = this.state;
        const { showGroupingConfig } = this.props;
        const variants = groupInfo
            ? Object.values(groupInfo).sort((a, b) => {
                var _a, _b, _c, _d;
                return a.hash && !b.hash
                    ? -1
                    : (_d = (_a = a.description) === null || _a === void 0 ? void 0 : _a.toLowerCase().localeCompare((_c = (_b = b.description) === null || _b === void 0 ? void 0 : _b.toLowerCase()) !== null && _c !== void 0 ? _c : '')) !== null && _d !== void 0 ? _d : 1;
            })
            : [];
        return (<react_1.Fragment>
        {showGroupingConfig && this.renderGroupConfigSelect()}

        {loading ? (<loadingIndicator_1.default />) : (variants.map((variant, index) => (<react_1.Fragment key={variant.key}>
              <groupingVariant_1.default variant={variant} showGroupingConfig={showGroupingConfig}/>
              {index < variants.length - 1 && <VariantDivider />}
            </react_1.Fragment>)))}
      </react_1.Fragment>);
    }
    renderLoading() {
        return this.renderBody();
    }
    renderBody() {
        const { isOpen } = this.state;
        const title = (<react_1.Fragment>
        {(0, locale_1.t)('Event Grouping Information')}
        {!isOpen && this.renderGroupInfoSummary()}
      </react_1.Fragment>);
        const actions = (<ToggleButton onClick={this.toggle} priority="link">
        {isOpen ? (0, locale_1.t)('Hide Details') : (0, locale_1.t)('Show Details')}
      </ToggleButton>);
        return (<eventDataSection_1.default type="grouping-info" title={title} actions={actions}>
        {isOpen && this.renderGroupInfo()}
      </eventDataSection_1.default>);
    }
}
const SummaryGroupedBy = (0, styled_1.default)('small') `
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    display: block;
    margin: 0 !important;
  }
`;
const ToggleButton = (0, styled_1.default)(button_1.default) `
  font-weight: 700;
  color: ${p => p.theme.subText};
  &:hover,
  &:focus {
    color: ${p => p.theme.textColor};
  }
`;
const GroupConfigWrapper = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(1.5)};
  margin-top: -${(0, space_1.default)(1)};
`;
exports.GroupingConfigItem = (0, styled_1.default)('span') `
  font-family: ${p => p.theme.text.familyMono};
  opacity: ${p => (p.isHidden ? 0.5 : null)};
  font-weight: ${p => (p.isActive ? 'bold' : null)};
  font-size: ${p => p.theme.fontSizeSmall};
`;
const VariantDivider = (0, styled_1.default)('hr') `
  padding-top: ${(0, space_1.default)(1)};
  border-top: 1px solid ${p => p.theme.border};
`;
exports.default = (0, withOrganization_1.default)(EventGroupingInfo);
//# sourceMappingURL=index.jsx.map