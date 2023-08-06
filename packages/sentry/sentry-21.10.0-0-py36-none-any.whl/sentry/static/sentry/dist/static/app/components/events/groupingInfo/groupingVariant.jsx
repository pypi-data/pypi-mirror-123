Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const capitalize_1 = (0, tslib_1.__importDefault)(require("lodash/capitalize"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const keyValueList_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/keyValueList"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("app/types");
const groupingComponent_1 = (0, tslib_1.__importDefault)(require("./groupingComponent"));
const utils_1 = require("./utils");
function addFingerprintInfo(data, variant) {
    if (variant.matched_rule) {
        data.push([
            (0, locale_1.t)('Fingerprint rule'),
            <TextWithQuestionTooltip key="type">
        {variant.matched_rule}
        <questionTooltip_1.default size="xs" position="top" title={(0, locale_1.t)('The server-side fingerprinting rule that produced the fingerprint.')}/>
      </TextWithQuestionTooltip>,
        ]);
    }
    if (variant.values) {
        data.push([(0, locale_1.t)('Fingerprint values'), variant.values]);
    }
    if (variant.client_values) {
        data.push([
            (0, locale_1.t)('Client fingerprint values'),
            <TextWithQuestionTooltip key="type">
        {variant.client_values}
        <questionTooltip_1.default size="xs" position="top" title={(0, locale_1.t)('The client sent a fingerprint that was overridden by a server-side fingerprinting rule.')}/>
      </TextWithQuestionTooltip>,
        ]);
    }
}
class GroupVariant extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            showNonContributing: false,
        };
        this.handleShowNonContributing = () => {
            this.setState({ showNonContributing: true });
        };
        this.handleHideNonContributing = () => {
            this.setState({ showNonContributing: false });
        };
    }
    getVariantData() {
        var _a, _b;
        const { variant, showGroupingConfig } = this.props;
        const data = [];
        let component;
        if (!this.state.showNonContributing && variant.hash === null) {
            return [data, component];
        }
        if (variant.hash !== null) {
            data.push([
                (0, locale_1.t)('Hash'),
                <TextWithQuestionTooltip key="hash">
          <Hash>{variant.hash}</Hash>
          <questionTooltip_1.default size="xs" position="top" title={(0, locale_1.t)('Events with the same hash are grouped together')}/>
        </TextWithQuestionTooltip>,
            ]);
        }
        if (variant.hashMismatch) {
            data.push([
                (0, locale_1.t)('Hash mismatch'),
                (0, locale_1.t)('hashing algorithm produced a hash that does not match the event'),
            ]);
        }
        switch (variant.type) {
            case types_1.EventGroupVariantType.COMPONENT:
                component = variant.component;
                data.push([
                    (0, locale_1.t)('Type'),
                    <TextWithQuestionTooltip key="type">
            {variant.type}
            <questionTooltip_1.default size="xs" position="top" title={(0, locale_1.t)('Uses a complex grouping algorithm taking event data into account')}/>
          </TextWithQuestionTooltip>,
                ]);
                if (showGroupingConfig && ((_a = variant.config) === null || _a === void 0 ? void 0 : _a.id)) {
                    data.push([(0, locale_1.t)('Grouping Config'), variant.config.id]);
                }
                break;
            case types_1.EventGroupVariantType.CUSTOM_FINGERPRINT:
                data.push([
                    (0, locale_1.t)('Type'),
                    <TextWithQuestionTooltip key="type">
            {variant.type}
            <questionTooltip_1.default size="xs" position="top" title={(0, locale_1.t)('Overrides the default grouping by a custom fingerprinting rule')}/>
          </TextWithQuestionTooltip>,
                ]);
                addFingerprintInfo(data, variant);
                break;
            case types_1.EventGroupVariantType.SALTED_COMPONENT:
                component = variant.component;
                data.push([
                    (0, locale_1.t)('Type'),
                    <TextWithQuestionTooltip key="type">
            {variant.type}
            <questionTooltip_1.default size="xs" position="top" title={(0, locale_1.t)('Uses a complex grouping algorithm taking event data and a fingerprint into account')}/>
          </TextWithQuestionTooltip>,
                ]);
                addFingerprintInfo(data, variant);
                if (showGroupingConfig && ((_b = variant.config) === null || _b === void 0 ? void 0 : _b.id)) {
                    data.push([(0, locale_1.t)('Grouping Config'), variant.config.id]);
                }
                break;
            default:
                break;
        }
        if (component) {
            data.push([
                (0, locale_1.t)('Grouping'),
                <GroupingTree key={component.id}>
          <groupingComponent_1.default component={component} showNonContributing={this.state.showNonContributing}/>
        </GroupingTree>,
            ]);
        }
        return [data, component];
    }
    renderTitle() {
        var _a, _b, _c;
        const { variant } = this.props;
        const isContributing = variant.hash !== null;
        let title;
        if (isContributing) {
            title = (0, locale_1.t)('Contributing variant');
        }
        else {
            const hint = (_a = variant.component) === null || _a === void 0 ? void 0 : _a.hint;
            if (hint) {
                title = (0, locale_1.t)('Non-contributing variant: %s', hint);
            }
            else {
                title = (0, locale_1.t)('Non-contributing variant');
            }
        }
        return (<tooltip_1.default title={title}>
        <VariantTitle>
          <ContributionIcon isContributing={isContributing}/>
          {(0, locale_1.t)('By')}{' '}
          {(_c = (_b = variant.description) === null || _b === void 0 ? void 0 : _b.split(' ').map(i => (0, capitalize_1.default)(i)).join(' ')) !== null && _c !== void 0 ? _c : (0, locale_1.t)('Nothing')}
        </VariantTitle>
      </tooltip_1.default>);
    }
    renderContributionToggle() {
        const { showNonContributing } = this.state;
        return (<ContributingToggle merged active={showNonContributing ? 'all' : 'relevant'}>
        <button_1.default barId="relevant" size="xsmall" onClick={this.handleHideNonContributing}>
          {(0, locale_1.t)('Contributing values')}
        </button_1.default>
        <button_1.default barId="all" size="xsmall" onClick={this.handleShowNonContributing}>
          {(0, locale_1.t)('All values')}
        </button_1.default>
      </ContributingToggle>);
    }
    render() {
        const [data, component] = this.getVariantData();
        return (<VariantWrapper>
        <Header>
          {this.renderTitle()}
          {(0, utils_1.hasNonContributingComponent)(component) && this.renderContributionToggle()}
        </Header>

        <keyValueList_1.default data={data.map(d => ({
                key: d[0],
                subject: d[0],
                value: d[1],
            }))} isContextData isSorted={false}/>
      </VariantWrapper>);
    }
}
const VariantWrapper = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(4)};
`;
const Header = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: ${(0, space_1.default)(2)};
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    display: block;
  }
`;
const VariantTitle = (0, styled_1.default)('h5') `
  font-size: ${p => p.theme.fontSizeMedium};
  margin: 0;
  display: flex;
  align-items: center;
`;
const ContributionIcon = (0, styled_1.default)((_a) => {
    var { isContributing } = _a, p = (0, tslib_1.__rest)(_a, ["isContributing"]);
    return isContributing ? (<icons_1.IconCheckmark size="sm" isCircled color="green300" {...p}/>) : (<icons_1.IconClose size="sm" isCircled color="red300" {...p}/>);
}) `
  margin-right: ${(0, space_1.default)(1)};
`;
const ContributingToggle = (0, styled_1.default)(buttonBar_1.default) `
  justify-content: flex-end;
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    margin-top: ${(0, space_1.default)(0.5)};
  }
`;
const GroupingTree = (0, styled_1.default)('div') `
  color: ${p => p.theme.textColor};
`;
const TextWithQuestionTooltip = (0, styled_1.default)('div') `
  display: grid;
  align-items: center;
  grid-template-columns: max-content min-content;
  grid-gap: ${(0, space_1.default)(0.5)};
`;
const Hash = (0, styled_1.default)('span') `
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    ${overflowEllipsis_1.default};
    width: 210px;
  }
`;
exports.default = GroupVariant;
//# sourceMappingURL=groupingVariant.jsx.map