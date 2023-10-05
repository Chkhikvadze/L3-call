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

  const { contacts } = useContacts()

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
          {contacts?.map((group: any) => {
            return (
              <TempCard
                key={group.id}
                name={group.name}
                description={group.description}
                // onDeleteClick={() => deleteGroupHandler(group.id)}
              />
            )
          })}
        </StyledCardsWrapper>
      </ComponentsWrapper>
    </StyledSectionWrapper>
  )
}

export default Contacts
