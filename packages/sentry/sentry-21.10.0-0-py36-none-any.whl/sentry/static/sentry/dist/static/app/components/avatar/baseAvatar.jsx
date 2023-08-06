Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const qs = (0, tslib_1.__importStar)(require("query-string"));
const backgroundAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/backgroundAvatar"));
const letterAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/letterAvatar"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const gravatar_1 = (0, tslib_1.__importDefault)(require("./gravatar"));
const styles_1 = require("./styles");
const DEFAULT_GRAVATAR_SIZE = 64;
const ALLOWED_SIZES = [20, 32, 36, 48, 52, 64, 80, 96, 120];
const DEFAULT_REMOTE_SIZE = 120;
// Note: Avatar will not always be a child of a flex layout, but this seems like a
// sensible default.
const StyledBaseAvatar = (0, styled_1.default)('span') `
  flex-shrink: 0;
  border-radius: ${p => (p.round ? '50%' : '3px')};
  border: ${p => (p.suggested ? `1px dashed ${p.theme.gray400}` : 'none')};
  background-color: ${p => p.loaded ? p.theme.background : 'background-color: rgba(200, 200, 200, 0.1);'};
`;
const defaultProps = {
    // No default size to ease transition from CSS defined sizes
    // size: 64,
    style: {},
    /**
     * Enable to display tooltips.
     */
    hasTooltip: false,
    /**
     * The type of avatar being rendered.
     */
    type: 'letter_avatar',
    /**
     * Path to uploaded avatar (differs based on model type)
     */
    uploadPath: 'avatar',
    /**
     * Should avatar be round instead of a square
     */
    round: false,
};
class BaseAvatar extends React.Component {
    constructor(props) {
        super(props);
        this.getRemoteImageSize = () => {
            const { remoteImageSize, size } = this.props;
            // Try to make sure remote image size is >= requested size
            // If requested size > allowed size then use the largest allowed size
            const allowed = size &&
                (ALLOWED_SIZES.find(allowedSize => allowedSize >= size) ||
                    ALLOWED_SIZES[ALLOWED_SIZES.length - 1]);
            return remoteImageSize || allowed || DEFAULT_GRAVATAR_SIZE;
        };
        this.buildUploadUrl = () => {
            const { uploadPath, uploadId } = this.props;
            return `/${uploadPath || 'avatar'}/${uploadId}/?${qs.stringify({
                s: DEFAULT_REMOTE_SIZE,
            })}`;
        };
        this.handleLoad = () => {
            this.setState({ showBackupAvatar: false, hasLoaded: true });
        };
        this.handleError = () => {
            this.setState({ showBackupAvatar: true, loadError: true, hasLoaded: true });
        };
        this.renderImg = () => {
            if (this.state.loadError) {
                return null;
            }
            const { type, round, gravatarId, suggested } = this.props;
            const eventProps = {
                onError: this.handleError,
                onLoad: this.handleLoad,
            };
            if (type === 'gravatar') {
                return (<gravatar_1.default placeholder={this.props.default} gravatarId={gravatarId} round={round} remoteSize={DEFAULT_REMOTE_SIZE} suggested={suggested} grayscale={suggested} {...eventProps}/>);
            }
            if (type === 'upload') {
                return (<Image round={round} src={this.buildUploadUrl()} {...eventProps} suggested={suggested} grayscale={suggested}/>);
            }
            if (type === 'background') {
                return this.renderBackgroundAvatar();
            }
            return this.renderLetterAvatar();
        };
        this.state = {
            showBackupAvatar: false,
            hasLoaded: props.type !== 'upload',
            loadError: false,
        };
    }
    renderLetterAvatar() {
        const { title, letterId, round, suggested } = this.props;
        return (<letterAvatar_1.default round={round} displayName={title} identifier={letterId} suggested={suggested}/>);
    }
    renderBackgroundAvatar() {
        const { round, suggested } = this.props;
        return <backgroundAvatar_1.default round={round} suggested={suggested}/>;
    }
    render() {
        const _a = this.props, { className, style, round, hasTooltip, size, suggested, tooltip, tooltipOptions, forwardedRef, type } = _a, props = (0, tslib_1.__rest)(_a, ["className", "style", "round", "hasTooltip", "size", "suggested", "tooltip", "tooltipOptions", "forwardedRef", "type"]);
        let sizeStyle = {};
        if (size) {
            sizeStyle = {
                width: `${size}px`,
                height: `${size}px`,
            };
        }
        return (<tooltip_1.default title={tooltip} disabled={!hasTooltip} {...tooltipOptions}>
        <StyledBaseAvatar data-test-id={`${type}-avatar`} ref={forwardedRef} loaded={this.state.hasLoaded} className={(0, classnames_1.default)('avatar', className)} round={!!round} suggested={!!suggested} style={Object.assign(Object.assign({}, sizeStyle), style)} {...props}>
          {this.state.showBackupAvatar && this.renderLetterAvatar()}
          {this.renderImg()}
        </StyledBaseAvatar>
      </tooltip_1.default>);
    }
}
BaseAvatar.defaultProps = defaultProps;
exports.default = BaseAvatar;
const Image = (0, styled_1.default)('img') `
  ${styles_1.imageStyle};
`;
//# sourceMappingURL=baseAvatar.jsx.map