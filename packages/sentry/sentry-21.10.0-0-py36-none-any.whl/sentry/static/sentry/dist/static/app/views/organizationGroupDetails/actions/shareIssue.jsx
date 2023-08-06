Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/actions/button"));
const autoSelectText_1 = (0, tslib_1.__importDefault)(require("app/components/autoSelectText"));
const button_2 = (0, tslib_1.__importDefault)(require("app/components/button"));
const clipboard_1 = (0, tslib_1.__importDefault)(require("app/components/clipboard"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const dropdownLink_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownLink"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const switchButton_1 = (0, tslib_1.__importDefault)(require("app/components/switchButton"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
class ShareUrlContainer extends React.Component {
    constructor() {
        super(...arguments);
        // Select URL when its container is clicked
        this.handleCopyClick = () => {
            var _a;
            (_a = this.urlRef) === null || _a === void 0 ? void 0 : _a.selectText();
        };
    }
    render() {
        const { shareUrl, onConfirming, onCancel, onConfirm } = this.props;
        return (<UrlContainer>
        <TextContainer>
          <StyledAutoSelectText ref={ref => (this.urlRef = ref)}>
            {shareUrl}
          </StyledAutoSelectText>
        </TextContainer>

        <clipboard_1.default hideUnsupported value={shareUrl}>
          <ClipboardButton title={(0, locale_1.t)('Copy to clipboard')} borderless size="xsmall" onClick={this.handleCopyClick} icon={<icons_1.IconCopy />}/>
        </clipboard_1.default>

        <confirm_1.default message={(0, locale_1.t)('You are about to regenerate a new shared URL. Your previously shared URL will no longer work. Do you want to continue?')} onCancel={onCancel} onConfirming={onConfirming} onConfirm={onConfirm}>
          <ReshareButton title={(0, locale_1.t)('Generate new URL')} borderless size="xsmall" icon={<icons_1.IconRefresh />}/>
        </confirm_1.default>
      </UrlContainer>);
    }
}
class ShareIssue extends React.Component {
    constructor() {
        super(...arguments);
        this.hasConfirmModal = false;
        this.handleToggleShare = (e) => {
            e.preventDefault();
            this.props.onToggle();
        };
        this.handleOpen = () => {
            const { loading, isShared, onToggle } = this.props;
            if (!loading && !isShared) {
                // Starts sharing as soon as dropdown is opened
                onToggle();
            }
        };
        // State of confirm modal so we can keep dropdown menu opn
        this.handleConfirmCancel = () => {
            this.hasConfirmModal = false;
        };
        this.handleConfirmReshare = () => {
            this.hasConfirmModal = true;
        };
    }
    render() {
        const { loading, isShared, shareUrl, onReshare, disabled } = this.props;
        return (<dropdownLink_1.default shouldIgnoreClickOutside={() => this.hasConfirmModal} customTitle={<button_1.default disabled={disabled}>
            <DropdownTitleContent>
              <IndicatorDot isShared={isShared}/>
              {(0, locale_1.t)('Share')}
            </DropdownTitleContent>

            <icons_1.IconChevron direction="down" size="xs"/>
          </button_1.default>} onOpen={this.handleOpen} disabled={disabled} keepMenuOpen>
        <DropdownContent>
          <Header>
            <Title>{(0, locale_1.t)('Enable public share link')}</Title>
            <switchButton_1.default isActive={isShared} size="sm" toggle={this.handleToggleShare}/>
          </Header>

          {loading && (<LoadingContainer>
              <loadingIndicator_1.default mini/>
            </LoadingContainer>)}

          {!loading && isShared && shareUrl && (<ShareUrlContainer shareUrl={shareUrl} onCancel={this.handleConfirmCancel} onConfirming={this.handleConfirmReshare} onConfirm={onReshare}/>)}
        </DropdownContent>
      </dropdownLink_1.default>);
    }
}
exports.default = ShareIssue;
const UrlContainer = (0, styled_1.default)('div') `
  display: flex;
  align-items: stretch;
  border: 1px solid ${p => p.theme.border};
  border-radius: ${(0, space_1.default)(0.5)};
`;
const LoadingContainer = (0, styled_1.default)('div') `
  display: flex;
  justify-content: center;
`;
const DropdownTitleContent = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  margin-right: ${(0, space_1.default)(0.5)};
`;
const DropdownContent = (0, styled_1.default)('li') `
  padding: ${(0, space_1.default)(1.5)} ${(0, space_1.default)(2)};

  > div:not(:last-of-type) {
    margin-bottom: ${(0, space_1.default)(1.5)};
  }
`;
const Header = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
`;
const Title = (0, styled_1.default)('h6') `
  margin: 0;
  padding-right: ${(0, space_1.default)(4)};
  white-space: nowrap;
`;
const IndicatorDot = (0, styled_1.default)('span') `
  display: inline-block;
  margin-right: ${(0, space_1.default)(0.5)};
  border-radius: 50%;
  width: 10px;
  height: 10px;
  background: ${p => (p.isShared ? p.theme.active : p.theme.border)};
`;
const StyledAutoSelectText = (0, styled_1.default)(autoSelectText_1.default) `
  flex: 1;
  padding: ${(0, space_1.default)(0.5)} 0 ${(0, space_1.default)(0.5)} ${(0, space_1.default)(0.75)};
  ${overflowEllipsis_1.default}
`;
const TextContainer = (0, styled_1.default)('div') `
  position: relative;
  display: flex;
  flex: 1;
  background-color: transparent;
  border-right: 1px solid ${p => p.theme.border};
  max-width: 288px;
`;
const ClipboardButton = (0, styled_1.default)(button_2.default) `
  border-radius: 0;
  border-right: 1px solid ${p => p.theme.border};
  height: 100%;

  &:hover {
    border-right: 1px solid ${p => p.theme.border};
  }
`;
const ReshareButton = (0, styled_1.default)(button_2.default) `
  height: 100%;
`;
//# sourceMappingURL=shareIssue.jsx.map