Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const createSampleEventButton_1 = (0, tslib_1.__importDefault)(require("app/views/onboarding/createSampleEventButton"));
const firstEventIndicator_1 = (0, tslib_1.__importDefault)(require("./firstEventIndicator"));
function FirstEventFooter({ organization, project, docsLink, docsOnClick, }) {
    return (<react_1.Fragment>
      <firstEventIndicator_1.default organization={organization} project={project} eventType="error">
        {({ indicator, firstEventButton }) => (<CTAFooter>
            <Actions gap={2}>
              {firstEventButton}
              <button_1.default external href={docsLink} onClick={docsOnClick}>
                {(0, locale_1.t)('View full documentation')}
              </button_1.default>
            </Actions>
            {indicator}
          </CTAFooter>)}
      </firstEventIndicator_1.default>
      <CTASecondary>
        {(0, locale_1.tct)('Just want to poke around before getting too cozy with the SDK? [sample:View a sample event for this SDK] and finish setup later.', {
            sample: (<createSampleEventButton_1.default project={project} source="onboarding" priority="link"/>),
        })}
      </CTASecondary>
    </react_1.Fragment>);
}
exports.default = FirstEventFooter;
const CTAFooter = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
  margin: ${(0, space_1.default)(2)} 0;
  margin-top: ${(0, space_1.default)(4)};
`;
const CTASecondary = (0, styled_1.default)('p') `
  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeMedium};
  margin: 0;
  max-width: 500px;
`;
const Actions = (0, styled_1.default)(buttonBar_1.default) `
  display: inline-grid;
  justify-self: start;
`;
//# sourceMappingURL=firstEventFooter.jsx.map