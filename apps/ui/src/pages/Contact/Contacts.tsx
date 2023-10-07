import { useNavigate } from 'react-router-dom'

import { ButtonPrimary } from 'components/Button/Button'
import ComponentsWrapper from 'components/ComponentsWrapper/ComponentsWrapper'

import { StyledCardsWrapper } from 'pages/Agents/Agents'

import {
  StyledHeaderGroup,
  StyledSectionTitle,
  StyledSectionWrapper,
} from 'pages/Home/homeStyle.css'
import { useContacts } from './useContacts'
import TempCard from 'pages/Group/TempCard'

const Contacts = () => {
  const navigate = useNavigate()

  const { contacts, deleteContactHandler } = useContacts()

  return (
    <StyledSectionWrapper>
      <StyledHeaderGroup className='header_group'>
        <div>
          <StyledSectionTitle>Contacts</StyledSectionTitle>
          {/* <StyledSectionDescription>
          Here is your datasource, a collection of databases, APIs, files, and more.
        </StyledSectionDescription> */}
        </div>
        <div>
          <ButtonPrimary onClick={() => navigate('/contacts/create-contact')} size={'small'}>
            Add Contact
          </ButtonPrimary>
        </div>
      </StyledHeaderGroup>

      <ComponentsWrapper noPadding>
        <StyledCardsWrapper>
          {contacts?.map((contact: any) => {
            return (
              <TempCard
                key={contact.id}
                name={contact.name}
                description={contact.description}
                onDeleteClick={() => deleteContactHandler(contact.id)}
                onEditClick={() => navigate(`/contacts/${contact.id}/edit-contact`)}
              />
            )
          })}
        </StyledCardsWrapper>
      </ComponentsWrapper>
    </StyledSectionWrapper>
  )
}

export default Contacts
