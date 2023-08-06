Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const item_1 = (0, tslib_1.__importDefault)(require("app/components/activity/item"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const body_1 = (0, tslib_1.__importDefault)(require("./body"));
const editorTools_1 = (0, tslib_1.__importDefault)(require("./editorTools"));
const header_1 = (0, tslib_1.__importDefault)(require("./header"));
const input_1 = (0, tslib_1.__importDefault)(require("./input"));
function Note(props) {
    const [editing, setEditing] = (0, react_1.useState)(false);
    const { modelId, user, dateCreated, text, authorName, hideDate, minHeight, showTime, projectSlugs, onDelete, onCreate, onUpdate, } = props;
    const activityItemProps = {
        hideDate,
        showTime,
        id: `activity-item-${modelId}`,
        author: {
            type: 'user',
            user,
        },
        date: dateCreated,
    };
    if (!editing) {
        const header = (<header_1.default {...{ authorName, user }} onEdit={() => setEditing(true)} onDelete={() => onDelete(props)}/>);
        return (<ActivityItemWithEditing {...activityItemProps} header={header}>
        <body_1.default text={text}/>
      </ActivityItemWithEditing>);
    }
    // When editing, `NoteInput` has its own header, pass render func to control
    // rendering of bubble body
    return (<ActivityItemNote {...activityItemProps}>
      {() => (<input_1.default {...{ modelId, minHeight, text, projectSlugs }} onEditFinish={() => setEditing(false)} onUpdate={note => {
                onUpdate(note, props);
                setEditing(false);
            }} onCreate={note => onCreate === null || onCreate === void 0 ? void 0 : onCreate(note)}/>)}
    </ActivityItemNote>);
}
const ActivityItemNote = (0, styled_1.default)(item_1.default) `
  /* this was nested under ".activity-note.activity-bubble" */
  ul {
    list-style: disc;
  }

  h1,
  h2,
  h3,
  h4,
  p,
  ul:not(.nav),
  ol,
  pre,
  hr,
  blockquote {
    margin-bottom: ${(0, space_1.default)(2)};
  }

  ul:not(.nav),
  ol {
    padding-left: 20px;
  }

  p {
    a {
      word-wrap: break-word;
    }
  }

  blockquote {
    font-size: 15px;
    border-left: 5px solid ${p => p.theme.innerBorder};
    padding-left: ${(0, space_1.default)(1)};
    margin-left: 0;
  }
`;
const ActivityItemWithEditing = (0, styled_1.default)(ActivityItemNote) `
  &:hover {
    ${editorTools_1.default} {
      display: inline-block;
    }
  }
`;
exports.default = Note;
//# sourceMappingURL=index.jsx.map