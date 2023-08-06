Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const utils_1 = require("app/components/events/contexts/utils");
const notAvailable_1 = (0, tslib_1.__importDefault)(require("app/components/notAvailable"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_2 = require("app/utils");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const imageVisualization_1 = (0, tslib_1.__importDefault)(require("./imageVisualization"));
function Modal({ eventAttachment, orgSlug, projectSlug, Header, Body, Footer, event, onDelete, downloadUrl, }) {
    const { dateCreated, size, mimetype } = eventAttachment;
    return (<react_1.Fragment>
      <Header closeButton>{(0, locale_1.t)('Screenshot')}</Header>
      <Body>
        <GeralInfo>
          <Label coloredBg>{(0, locale_1.t)('Date Created')}</Label>
          <Value coloredBg>
            {dateCreated ? (<react_1.Fragment>
                <dateTime_1.default date={(0, getDynamicText_1.default)({
                value: dateCreated,
                fixed: new Date(1508208080000),
            })}/>
                {(0, utils_1.getRelativeTimeFromEventDateCreated)(event.dateCreated ? event.dateCreated : event.dateReceived, dateCreated, false)}
              </react_1.Fragment>) : (<notAvailable_1.default />)}
          </Value>

          <Label>{(0, locale_1.t)('Name')}</Label>
          <Value>{(0, locale_1.t)('Screenshot')}</Value>

          <Label coloredBg>{(0, locale_1.t)('Size')}</Label>
          <Value coloredBg>
            {(0, utils_2.defined)(size) ? (0, utils_2.formatBytesBase2)(size) : <notAvailable_1.default />}
          </Value>

          <Label>{(0, locale_1.t)('MIME Type')}</Label>
          <Value>{mimetype !== null && mimetype !== void 0 ? mimetype : <notAvailable_1.default />}</Value>
        </GeralInfo>

        <StyledImageVisualization attachment={eventAttachment} orgId={orgSlug} projectId={projectSlug} event={event}/>
      </Body>
      <Footer>
        <buttonBar_1.default gap={1}>
          <confirm_1.default confirmText={(0, locale_1.t)('Delete')} header={(0, locale_1.t)('Screenshots help identify what the user saw when the event happened')} message={(0, locale_1.t)('Are you sure you wish to delete this screenshot?')} priority="danger" onConfirm={onDelete}>
            <button_1.default priority="danger">{(0, locale_1.t)('Delete')}</button_1.default>
          </confirm_1.default>
          <button_1.default href={downloadUrl}>{(0, locale_1.t)('Download')}</button_1.default>
        </buttonBar_1.default>
      </Footer>
    </react_1.Fragment>);
}
exports.default = Modal;
const GeralInfo = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content 1fr;
  margin-bottom: ${(0, space_1.default)(3)};
`;
const Label = (0, styled_1.default)('div') `
  color: ${p => p.theme.textColor};
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(1.5)} ${(0, space_1.default)(1)} ${(0, space_1.default)(1)};
  ${p => p.coloredBg && `background-color: ${p.theme.backgroundSecondary};`}
`;
const Value = (0, styled_1.default)(Label) `
  white-space: pre-wrap;
  word-break: break-all;
  color: ${p => p.theme.subText};
  padding: ${(0, space_1.default)(1)};
  font-family: ${p => p.theme.text.familyMono};
  ${p => p.coloredBg && `background-color: ${p.theme.backgroundSecondary};`}
`;
const StyledImageVisualization = (0, styled_1.default)(imageVisualization_1.default) `
  img {
    border-radius: ${p => p.theme.borderRadius};
  }
`;
exports.modalCss = (0, react_2.css) `
  width: auto;
  height: 100%;
  max-width: 100%;
`;
//# sourceMappingURL=modal.jsx.map