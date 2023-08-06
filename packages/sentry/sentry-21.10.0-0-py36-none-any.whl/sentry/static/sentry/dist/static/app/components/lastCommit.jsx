Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const userAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/userAvatar"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const locale_1 = require("app/locale");
const unknownUser = {
    id: '',
    name: '',
    username: '??',
    email: '',
    avatarUrl: '',
    avatar: {
        avatarUuid: '',
        avatarType: 'letter_avatar',
    },
    ip_address: '',
};
function LastCommit({ commit, headerClass }) {
    function renderMessage(message) {
        if (!message) {
            return (0, locale_1.t)('No message provided');
        }
        const firstLine = message.split(/\n/)[0];
        if (firstLine.length > 100) {
            let truncated = firstLine.substr(0, 90);
            const words = truncated.split(/ /);
            // try to not have elipsis mid-word
            if (words.length > 1) {
                words.pop();
                truncated = words.join(' ');
            }
            return `${truncated}\u2026`;
        }
        return firstLine;
    }
    const commitAuthor = commit === null || commit === void 0 ? void 0 : commit.author;
    return (<div>
      <h6 className={headerClass}>Last commit</h6>
      <div className="commit">
        <div className="commit-avatar">
          <userAvatar_1.default user={commitAuthor || unknownUser}/>
        </div>
        <div className="commit-message truncate">{renderMessage(commit.message)}</div>
        <div className="commit-meta">
          <strong>{(commitAuthor === null || commitAuthor === void 0 ? void 0 : commitAuthor.name) || (0, locale_1.t)('Unknown Author')}</strong>
          &nbsp;
          <timeSince_1.default date={commit.dateCreated}/>
        </div>
      </div>
    </div>);
}
exports.default = LastCommit;
//# sourceMappingURL=lastCommit.jsx.map