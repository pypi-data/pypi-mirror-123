Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const utils_1 = require("../utils");
const statusTooltip_1 = (0, tslib_1.__importDefault)(require("./status/statusTooltip"));
const actions_1 = (0, tslib_1.__importDefault)(require("./actions"));
const information_1 = (0, tslib_1.__importDefault)(require("./information"));
function Candidate({ candidate, organization, projSlug, baseUrl, haveCandidatesAtLeastOneAction, hasReprocessWarning, onDelete, eventDateReceived, }) {
    const { source } = candidate;
    const isInternalSource = source === utils_1.INTERNAL_SOURCE;
    return (<react_1.Fragment>
      <Column>
        <statusTooltip_1.default candidate={candidate} hasReprocessWarning={hasReprocessWarning}/>
      </Column>

      <InformationColumn>
        <information_1.default candidate={candidate} isInternalSource={isInternalSource} eventDateReceived={eventDateReceived} hasReprocessWarning={hasReprocessWarning}/>
      </InformationColumn>

      {haveCandidatesAtLeastOneAction && (<ActionsColumn>
          <actions_1.default onDelete={onDelete} baseUrl={baseUrl} projSlug={projSlug} organization={organization} candidate={candidate} isInternalSource={isInternalSource}/>
        </ActionsColumn>)}
    </react_1.Fragment>);
}
exports.default = Candidate;
const Column = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const InformationColumn = (0, styled_1.default)(Column) `
  flex-direction: column;
  align-items: flex-start;
`;
const ActionsColumn = (0, styled_1.default)(Column) `
  justify-content: flex-end;
`;
//# sourceMappingURL=index.jsx.map