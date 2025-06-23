describe('Users Management', () => {
  beforeEach(() => {
    // Login as admin before each test
    cy.visit('http://localhost:3000/login')
    cy.get('input[name="username"]').type('admin')
    cy.get('input[name="password"]').type('admin123')
    cy.get('button[type="submit"]').click()
    cy.url().should('include', '/users')
  })

  it('should display users list for admin', () => {
    cy.get('table').should('exist')
    cy.contains('th', 'Username')
    cy.contains('th', 'Email')
    cy.contains('th', 'Created At')
    cy.contains('th', 'Actions')
  })

  it('should allow admin to delete a user', () => {
    // First create a user to delete
    cy.visit('http://localhost:3000/register')
    const username = `deleteuser${Date.now()}`
    cy.get('input[name="username"]').type(username)
    cy.get('input[name="email"]').type(`${username}@example.com`)
    cy.get('input[name="password"]').type('password123')
    cy.get('button[type="submit"]').click()

    // Login back as admin
    cy.visit('http://localhost:3000/login')
    cy.get('input[name="username"]').type('admin')
    cy.get('input[name="password"]').type('admin123')
    cy.get('button[type="submit"]').click()

    // Find and delete the user
    cy.contains('td', username)
      .parent()
      .find('button')
      .contains('Delete')
      .click()

    // Verify user is deleted
    cy.contains('td', username).should('not.exist')
  })

  it('should logout successfully', () => {
    cy.contains('button', 'Logout').click()
    cy.url().should('include', '/login')
  })
}) 