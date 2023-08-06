Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const avatar_1 = (0, tslib_1.__importDefault)(require("app/components/activity/item/avatar"));
const card_1 = (0, tslib_1.__importDefault)(require("app/components/card"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const callIfFunction_1 = require("app/utils/callIfFunction");
class QueryCard extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.handleClick = () => {
            const { onEventClick } = this.props;
            (0, callIfFunction_1.callIfFunction)(onEventClick);
        };
    }
    render() {
        const { title, subtitle, queryDetail, renderContextMenu, renderGraph, createdBy, dateStatus, } = this.props;
        return (<link_1.default data-test-id={`card-${title}`} onClick={this.handleClick} to={this.props.to}>
        <StyledQueryCard interactive>
          <QueryCardHeader>
            <QueryCardContent>
              <QueryTitle>{title}</QueryTitle>
              <QueryDetail>{queryDetail}</QueryDetail>
            </QueryCardContent>
            <AvatarWrapper>
              {createdBy ? (<avatar_1.default type="user" user={createdBy} size={34}/>) : (<avatar_1.default type="system" size={34}/>)}
            </AvatarWrapper>
          </QueryCardHeader>
          <QueryCardBody>{renderGraph()}</QueryCardBody>
          <QueryCardFooter>
            <DateSelected>
              {subtitle}
              {dateStatus ? (<DateStatus>
                  {(0, locale_1.t)('Edited')} {dateStatus}
                </DateStatus>) : null}
            </DateSelected>
            {renderContextMenu && renderContextMenu()}
          </QueryCardFooter>
        </StyledQueryCard>
      </link_1.default>);
    }
}
const AvatarWrapper = (0, styled_1.default)('span') `
  border: 3px solid ${p => p.theme.border};
  border-radius: 50%;
  height: min-content;
`;
const QueryCardContent = (0, styled_1.default)('div') `
  flex-grow: 1;
  overflow: hidden;
  margin-right: ${(0, space_1.default)(1)};
`;
const StyledQueryCard = (0, styled_1.default)(card_1.default) `
  justify-content: space-between;
  height: 100%;
  &:focus,
  &:hover {
    top: -1px;
  }
`;
const QueryCardHeader = (0, styled_1.default)('div') `
  display: flex;
  padding: ${(0, space_1.default)(1.5)} ${(0, space_1.default)(2)};
`;
const QueryTitle = (0, styled_1.default)('div') `
  color: ${p => p.theme.textColor};
  ${overflowEllipsis_1.default};
`;
const QueryDetail = (0, styled_1.default)('div') `
  font-family: ${p => p.theme.text.familyMono};
  font-size: ${p => p.theme.fontSizeSmall};
  color: ${p => p.theme.gray300};
  line-height: 1.5;
  ${overflowEllipsis_1.default};
`;
const QueryCardBody = (0, styled_1.default)('div') `
  background: ${p => p.theme.backgroundSecondary};
  max-height: 100px;
  height: 100%;
  overflow: hidden;
`;
const QueryCardFooter = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
`;
const DateSelected = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeSmall};
  display: grid;
  grid-column-gap: ${(0, space_1.default)(1)};
  ${overflowEllipsis_1.default};
  color: ${p => p.theme.textColor};
`;
const DateStatus = (0, styled_1.default)('span') `
  color: ${p => p.theme.purple300};
  padding-left: ${(0, space_1.default)(1)};
`;
exports.default = QueryCard;
//# sourceMappingURL=querycard.jsx.map