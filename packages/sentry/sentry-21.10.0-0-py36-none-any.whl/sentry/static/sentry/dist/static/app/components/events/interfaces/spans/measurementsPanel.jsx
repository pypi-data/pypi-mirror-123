Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const utils_1 = require("app/components/performance/waterfall/utils");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const utils_2 = require("app/utils");
const constants_1 = require("app/utils/performance/vitals/constants");
const utils_3 = require("./utils");
class MeasurementsPanel extends react_1.PureComponent {
    render() {
        const { event, generateBounds, dividerPosition } = this.props;
        const measurements = (0, utils_3.getMeasurements)(event);
        return (<Container style={{
                // the width of this component is shrunk to compensate for half of the width of the divider line
                width: `calc(${(0, utils_1.toPercent)(1 - dividerPosition)} - 0.5px)`,
            }}>
        {Array.from(measurements).map(([timestamp, verticalMark]) => {
                const bounds = (0, utils_3.getMeasurementBounds)(timestamp, generateBounds);
                const shouldDisplay = (0, utils_2.defined)(bounds.left) && (0, utils_2.defined)(bounds.width);
                if (!shouldDisplay || !bounds.isSpanVisibleInView) {
                    return null;
                }
                // Measurements are referred to by their full name `measurements.<name>`
                // here but are stored using their abbreviated name `<name>`. Make sure
                // to convert it appropriately.
                const vitals = Object.keys(verticalMark.marks).map(name => constants_1.WEB_VITAL_DETAILS[`measurements.${name}`]);
                // generate vertical marker label
                const acronyms = vitals.map(vital => vital.acronym);
                const lastAcronym = acronyms.pop();
                const label = acronyms.length
                    ? `${acronyms.join(', ')} & ${lastAcronym}`
                    : lastAcronym;
                // generate tooltip labe;l
                const longNames = vitals.map(vital => vital.name);
                const lastName = longNames.pop();
                const tooltipLabel = longNames.length
                    ? `${longNames.join(', ')} & ${lastName}`
                    : lastName;
                return (<LabelContainer key={String(timestamp)} failedThreshold={verticalMark.failedThreshold} label={label} tooltipLabel={tooltipLabel} left={(0, utils_1.toPercent)(bounds.left || 0)}/>);
            })}
      </Container>);
    }
}
const Container = (0, styled_1.default)('div') `
  position: relative;
  overflow: hidden;

  height: 20px;
`;
const StyledLabelContainer = (0, styled_1.default)('div') `
  position: absolute;
  top: 0;
  height: 100%;
  user-select: none;
  white-space: nowrap;
`;
const Label = (0, styled_1.default)('div') `
  transform: translateX(-50%);
  font-size: ${p => p.theme.fontSizeExtraSmall};
  font-weight: 600;
  ${p => (p.failedThreshold ? `color: ${p.theme.red300};` : null)}
`;
exports.default = MeasurementsPanel;
class LabelContainer extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            width: 1,
        };
        this.elementDOMRef = (0, react_1.createRef)();
    }
    componentDidMount() {
        const { current } = this.elementDOMRef;
        if (current) {
            // eslint-disable-next-line react/no-did-mount-set-state
            this.setState({
                width: current.clientWidth,
            });
        }
    }
    render() {
        const { left, label, tooltipLabel, failedThreshold } = this.props;
        return (<StyledLabelContainer ref={this.elementDOMRef} style={{
                left: `clamp(calc(0.5 * ${this.state.width}px), ${left}, calc(100% - 0.5 * ${this.state.width}px))`,
            }}>
        <Label failedThreshold={failedThreshold}>
          <tooltip_1.default title={tooltipLabel} position="top" containerDisplayMode="inline-block">
            {label}
          </tooltip_1.default>
        </Label>
      </StyledLabelContainer>);
    }
}
//# sourceMappingURL=measurementsPanel.jsx.map