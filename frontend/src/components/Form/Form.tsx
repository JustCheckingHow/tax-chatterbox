import React from 'react';
import styles from "./Form.module.scss";

interface FieldInfo {
  description: string;
  label: string;
  required: boolean;
  type: string;
  pattern?: string;
  visible?: boolean;
}

interface Section {
  label: string;
  content: { [key: string]: FieldInfo }[];
}

interface formProps {
  required_info: { section: Section }[];
  obtained_info: { [key: string]: any };
  setObtainedInfo: React.Dispatch<React.SetStateAction<{ [key: string]: any }>>;
}

const Form: React.FC<formProps> = ({ required_info, obtained_info, setObtainedInfo }) => {
  const renderField = (name: string, field: FieldInfo) => {
    if (field.visible === false) return null;

    const val = obtained_info[name] || '';
    const isChecked = val !== '';
    const type = field.type !== "string" ? field.type : "text";

    return (
      <li key={name} className={isChecked ? styles.checked : ""}>
        <div className={`${field.required ? styles.required : ""} ${styles.label}`}>{field.label}</div>
        <input
          type={type}
          value={val}
          onChange={(e) => setObtainedInfo((prev) => ({ ...prev, [name]: e.target.value }))}
          required={field.required}
          pattern={field.pattern}
        />
      </li>
    );
  };

  if (!required_info || !Array.isArray(required_info)) {
    return <div>Error: Invalid required_info data</div>;
  }

  return (
    <aside className={styles.form__aside}>
      <h3>Skompletowane dane</h3>
      {required_info.map((item, index) => {
        if (!item.section) return null;
        const { label, content } = item.section;
        return (
          <div key={index} id={label}>
            <h4>{label}</h4>
            <ul className={styles.form__ul}>
              {content.map((fieldObj) => {
                const [name, field] = Object.entries(fieldObj)[0];
                return renderField(name, field);
              })}
            </ul>
          </div>
        );
      })}
    </aside>
  );
};

export default Form;